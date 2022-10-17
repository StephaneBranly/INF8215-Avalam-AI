from avalam import *
import itertools
import json
import random
from heuristic.Genetic1Action import Genetic1Action
from heuristic.GeneticMultAction import GeneticMultAction
from heuristic.GeneticSingleLoop import GeneticSingleLoop

from utils import key_value_or_default

available_heuristics = [Genetic1Action, GeneticMultAction, GeneticSingleLoop]

class GeneticAgent(EvolvedAgent):
    def setup(self, agent, parser, args):
        self.individu = key_value_or_default(args, 'individu', -1)
        self.mode = key_value_or_default(args, 'mode', "train")
        self.save_path = key_value_or_default(args, 'save', "NN")
        self.rate = key_value_or_default(args, 'rate', 1)
        self.keep = key_value_or_default(args, 'keep', 20)
        self.heuristic = key_value_or_default(args, 'heuristic', "Genetic1Action")
        self.current_individu = None
        self.current_gen = key_value_or_default(args, 'generation', 0)
        self.current_heuristic = self.default_heuristic() # for play and train
        self.heuristics = dict()
        if self.mode == "train":
            self.matchs = [m for m in itertools.combinations(range(self.individu), 2)]
            self.load_heuristics_of_pool()
        elif self.mode == "play":
            if self.individu == -1:
                self.load_best_individu(self.current_gen)
            else:
                self.current_heuristic.load_from_json(f"{self.save_path}/gen{self.current_gen}.json", self.individu)
                self.current_individu = self.individu
        elif self.mode == "evaluate":
            self.load_best_individu(self.current_gen)
        if self.mode == "stats":
            self.current_heuristic.load_from_json(f"{self.save_path}/gen0.json", 0)
            self.generate_stats_file()
    
    def load_best_individu(self,gen):
        try:
            with open(f"{self.save_path}/gen{gen}.json") as fp:
                listObj = json.load(fp)
            scores = [cell['score'] for cell in listObj['gen']]
            individu = scores.index(max(scores))
            self.current_individu = individu
            self.current_heuristic.load_from_json(f"{self.save_path}/gen{gen}.json", individu)
        except BaseException as e:
            print(f"BaseException raised: {e}")
            print('No more generation')

    def load_heuristics_of_pool(self):
        if self.current_gen == 0:
            if len(self.heuristics.keys()) == 0: # first individu added, we generate a new file
                f = open(f"{self.save_path}/gen{self.current_gen}.json", "w")
                f.write('{ \"gen\": []}')
                f.close()
            for a in range(self.individu):
                if a == 0:
                    f = open(f"{self.save_path}/description.txt", "w")
                    f.write(f"Class     : {self.__class__.__name__}\n")
                    f.write(f"Heuristic : {self.heuristic}\n")
                    f.write(f"Individu  : {str(self.individu)}\n")
                    f.write(f"Keep      : {str(self.keep)}\n")
                    f.write(f"Mutation  : {str(self.rate)}\n")
                    f.close()
                    self.heuristics[a] = self.default_heuristic()
                else:
                    self.heuristics[a] = self.heuristics[0].clone()
                    self.heuristics[a].set_parameters([random.uniform(-1,1) for _ in range(len(self.heuristics[0]._functions))])
                self.heuristics[a].save_as_json(f"{self.save_path}/gen{self.current_gen}.json", a)
                
        self.scores = dict()
        for a in range(self.individu):
            self.scores[a] = 0
            self.load_agent(a, self.current_gen)

    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        if self.mode == "train":
            if player == -1:
                return self.play_agent(self.heuristics[self.matchs[game_id][1]], percepts, player, step, time_left)
            elif player == 1:
                return self.play_agent(self.heuristics[self.matchs[game_id][0]], percepts, player, step, time_left)
        else:
            return self.play_agent(self.current_heuristic, percepts, player, step, time_left)

    def play_agent(self, agent,percepts, player, step, time_left):
        """
        here define the action of your agent
        """
        pass

    def finished(self, steps, winner, reason="", player=None, game_id=None, pool_id=None):
        if self.mode == "train":
            player_winner = 1 if winner < 0 else 0 if winner > 0 else None
            if player == 1:
                if winner != 0:
                    self.scores[self.matchs[game_id][player_winner]]    += abs(winner)
                    self.scores[self.matchs[game_id][1-player_winner]]  -= abs(winner)

    def load_agent(self, individu, generation):
        if individu not in self.heuristics:
            self.heuristics[individu] = self.default_heuristic()
        self.heuristics[individu].load_from_json(f"{self.save_path}/gen{generation}.json", individu)
    
    def default_heuristic(self):
        """returns the agent's core (NN, Genetic Heuristic, ...)"""
        for heuristic in available_heuristics:
            if heuristic.__name__ == self.heuristic:
                return heuristic()
        error = f"heuristic {self.heuristic} not found in {[h.__name__ for h in available_heuristics]}"
        raise Exception(error)

    def save_stats(self):
        with open(f"{self.save_path}/gen{self.current_gen}.json") as f:
            listObj = json.load(f)
            for i in range(self.individu):
                listObj["gen"][i]["score"] = self.scores[i]
        with open(f"{self.save_path}/gen{self.current_gen}.json", 'w') as outfile:
            json.dump(listObj, outfile)

    def pool_ended(self, pool_results, player, pool_id=None):
        if self.mode == "train":
            if player == 1:
                self.save_stats()
                results = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
                f = open(f"{self.save_path}/gen{self.current_gen+1}.json", "w")
                f.write('{ \"gen\": []}')
                f.close()

                for l in range(self.individu):
                    father = self.default_heuristic()
                    father.load_from_json(f"{self.save_path}/gen{self.current_gen}.json", results[random.randint(0, self.individu*self.keep//100)][0])
                    mother = self.default_heuristic()
                    mother.load_from_json(f"{self.save_path}/gen{self.current_gen}.json", results[random.randint(0, self.individu*self.keep//100)][0])
                    child = father.crossover(mother)
                    child.mutate(self.rate/100)
                    
                    child.save_as_json(f"{self.save_path}/gen{self.current_gen+1}.json", l)
                self.current_gen += 1

                self.load_heuristics_of_pool()
        if self.mode == "evaluate":
            self.current_gen += 1
            self.load_best_individu(self.current_gen)
           
        return super().pool_ended(pool_results, player)

    def get_agent_id(self):
        """Return an identifier for this agent."""
        if self.mode == "train":
            return "Genetic Agent Training"
        elif self.mode == "evaluate" or self.mode == "play":
            return f"Genetic Agent #{self.current_individu} gen{self.current_gen} {self.save_path}"
        return "Genetic Agent"

    def generate_stats_file(self):
        return None

if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=-1, help="play : index of indiv if -1 take best | number of indiv per gen", type=int)
        parser.add_argument("-G", "--generation", default=0, help="play : index of gen | train : number of gen", type=int)
        parser.add_argument("-M", "--mode", default="train", help="train | play | evaluate | stats", type=str)
        parser.add_argument("-H", "--heuristic", default="Genetic1Action", help="Heuristic class name", type=str)
        parser.add_argument("-S","--save", default="NN_heuristic", help="path to save the NN", type=str)
        parser.add_argument("-R","--rate", default=1, help="mutation rate in percentage [0:100]", type=float)
        parser.add_argument("-K","--keep", default=10, help="percentage of agent we keep [0:100]", type=int)
    agent = GeneticAgent()
    agent_main(agent, argument_parser, agent.setup)