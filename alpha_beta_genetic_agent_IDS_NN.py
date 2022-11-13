from heuristic.SklearnHeuristic import HeuristicSklearn
from heuristic.NN_Heuristic import NN_Heuristic
from avalam import *

from heuristic.Heuristic import *
from strategies.AlphaBetaIDS import AlphaBetaIDS

class AlphaBetaIDSGeneticAgentNN(EvolvedAgent,AlphaBetaIDS):

    def __init__(self, only_useful = False, max_step=20):
        self.explored = 0
        self.only_useful = only_useful
        self.max_step=max_step
        self.agent = HeuristicSklearn()
        super().__init__()

    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        board = dict_to_improved_board(percepts)
        action = self.use_strategy(board, player, step, 60 , other_params={'heuristic': self.agent, 'max_step': self.max_step}, stats=False)
        print(action)
        # print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        return action

    def get_agent_id(self):
        return super().get_agent_id() + "_NN"

if __name__ == "__main__":
    agent = AlphaBetaIDSGeneticAgentNN()
    agent_main(agent, agent.argument_parser, agent.setup)