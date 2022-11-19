from avalam import *
from genetic_player import GeneticAgent
from heuristic.Heuristic import *
from strategies.AlphaBetaIDS import AlphaBetaIDS
import time

class AlphaBetaIDSGeneticAgent(GeneticAgent, AlphaBetaIDS):

    def __init__(self, only_useful = False, max_step=10):
        self.explored = 0
        self.only_useful = only_useful
        self.max_step=max_step
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left, stats=True):
        board = dict_to_improved_board(percepts, True)
        start = time.time()
        if time_left:
            time_to_play = time_left/((34-step)/2) if step < 34 else time_left/2
        action = self.use_strategy(board, player, step, 6000000 if time_left == None else time_to_play, other_params={'heuristic': agent, 'max_step': self.max_step}, stats=stats)
        # print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        #print("time credit", time_left - (time.time() - start),"/900")
        return action

if __name__ == "__main__":
    agent = AlphaBetaIDSGeneticAgent()
    agent_main(agent, agent.argument_parser, agent.setup)