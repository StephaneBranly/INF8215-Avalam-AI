from avalam import *
import itertools
import json
import random

class Genetic_agent(EvolutedAgent):
    
    def setup(self, agent, parser, args):
        self.nb_individu = args.individu
        self.gen = args.generation
        self.mode = args.mode
        self.save = args.save
        self.rate = args.rate
        self.keep = args.keep
        self.current_individu = None
        self.current_gen = 0
        self.added_players = []
        self.agent_p1 = self.default_agent()
        self.agent_m1 = self.default_agent()
        if self.mode == "train":
            self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

            self.current_match = None
            self.scores = dict()
            for a in range(self.nb_individu):
                self.scores[a] = 0
            self.load_match()
        elif self.mode == "play":
            if args.individu == -1:
                self.load_best_individu(self.gen)
            else:
                self.agent_p1.load_from_json(f"{self.save}/gen{self.gen}.json", args.individu)
        elif self.mode == "evaluate":
            self.load_best_individu(self.current_gen)
    


    def load_best_individu(self,gen):
        try:
            with open(f"{self.save}/gen{gen}.json") as fp:
                listObj = json.load(fp)
            scores = [cell['score'] for cell in listObj['gen']]
            individu = scores.index(max(scores))
            print(f"Best individu of generation {gen} is {individu}")
            self.agent_p1.load_from_json(f"{self.save}/gen{self.gen}.json", individu)
        except:
            print('No more generation')


    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        if self.mode == "train":
            if player == -1:
                return self.play_agent(self.agent_m1, percepts, player, step, time_left)
            elif player == 1:
                return self.play_agent(self.agent_p1, percepts, player, step, time_left)
        else:
            return self.play_agent(self.agent_p1, percepts, player, step, time_left)

    def play_agent(self, agent,percepts, player, step, time_left):
        """
        here define the action of your agent
        """
        pass

    def finished(self, steps, winner, reason="", player=None):
        if self.mode == "train":
            player_winner = 0 if winner < 0 else 1 if winner > 0 else None
            if player == 1:
                if winner != 0:
                    self.scores[self.current_match[player_winner]] += abs(winner)
                    self.scores[self.current_match[1-player_winner]] -= abs(winner)
                if len(self.matchs):
                    self.load_match()

    def load_match(self):
        self.current_match = self.matchs.pop(0)
        if self.gen == 0: # case of the first generation, we create random NN
            if len(self.added_players) == 0: # first individu added, we generate a new file
                f = open(f"{self.save}/gen{self.gen}.json", "w")
                f.write('{ \"gen\": []}')
                f.close()
            if self.current_match[0] not in self.added_players: # we add player -1 if not already added
                self.agent_m1 = self.default_agent()
                self.agent_m1.save_as_json(f"{self.save}/gen{self.gen}.json", self.current_match[0])
                self.added_players.append(self.current_match[0])
            if self.current_match[1] not in self.added_players: # we add player 1 if not already added
                self.agent_p1 = self.default_agent()
                self.agent_p1.save_as_json(f"{self.save}/gen{self.gen}.json", self.current_match[1])
                self.added_players.append(self.current_match[1])
        else: # case of the next generations, we load the NN of the previous generation
            self.agent_m1.load_from_json(f"{self.save}/gen{self.gen}.json", self.current_match[0])
            self.agent_p1.load_from_json(f"{self.save}/gen{self.gen}.json", self.current_match[1])
    
    def default_agent(self):
        """returns the agent's core (NN, genetic Heuristic, ...)"""
        pass

    def save_stats(self):
        with open(f"{self.save}/gen{self.gen}.json") as f:
            listObj = json.load(f)
            for i in range(self.nb_individu):
                listObj["gen"][i]["score"] = self.scores[i]
        with open(f"{self.save}/gen{self.gen}.json", 'w') as outfile:
            json.dump(listObj, outfile)

    def pool_ended(self, pool, player):
        if self.mode == "train":
            if player == 1:
                print(self.scores)
                self.save_stats()
                results = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
                f = open(f"{self.save}/gen{self.gen+1}.json", "w")
                f.write('{ \"gen\": []}')
                f.close()
                for l in range(self.nb_individu):
                    father = self.default_agent()
                    father.load_from_json(f"{self.save}/gen{self.gen}.json", results[random.randint(0, self.nb_individu*100//self.keep)][0])
                    mother = self.default_agent()
                    mother.load_from_json(f"{self.save}/gen{self.gen}.json", results[random.randint(0, self.nb_individu*100//self.keep)][0])
                    child = father.crossover(mother)
                    child.mutate(self.rate)
                    
                    child.save_as_json(f"{self.save}/gen{self.gen+1}.json", l)
                self.gen += 1

                self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

                self.current_match = None
                self.scores = dict()
                for a in range(self.nb_individu):
                    self.scores[a] = 0
                self.load_match()
        elif self.mode == "evaluate":
            self.current_gen += 1
            self.load_best_individu(self.current_gen)
           
        return super().pool_ended(pool, player)


if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=-1, help="play : index of indiv if -1 take best | number of indiv per gen", type=int)
        parser.add_argument("-G", "--generation", default=0, help="play : index of gen | train : number of gen", type=int)
        parser.add_argument("-M", "--mode", default="train", help="train | play | evaluate", type=str)
        parser.add_argument("-S","--save", default="NN_heuristic", help="path to save the NN", type=str)
        parser.add_argument("-R","--rate", default=0.01, help="mutation rate", type=float)
        parser.add_argument("-K","--keep", default=10, help="percentage of agent we keep [0:100]", type=int)
    agent = Genetic_agent()
    agent_main(agent, argument_parser, agent.setup)