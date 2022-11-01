import random
from avalam import *
from genetic_player import GeneticAgent
from heuristic.Heuristic import *
from strategies.WorstMove import WorstMove

class WorstMoveGeneticAgent(GeneticAgent, WorstMove):

    def __init__(self, only_useful = False):
        self.explored = 0
        self.only_useful = only_useful
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left, stats=False):
        board = dict_to_improved_board(percepts)
        action = self.use_strategy(board, player, step, 10, other_params={'heuristic': agent}, stats=stats)
        # print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        return action

    def get_agent_id(self):
        return super().get_agent_id() + "_WorstMove"

if __name__ == "__main__":
    agent = WorstMoveGeneticAgent()
    agent_main(agent, agent.argument_parser, agent.setup)