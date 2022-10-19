from avalam import *
from genetic_player import GeneticAgent
from heuristic.Heuristic import *
from strategies.AlphaBeta import AlphaBeta

class AlphaBetaGeneticAgent(GeneticAgent, AlphaBeta):

    def __init__(self, only_useful = False):
        self.explored = 0
        self.only_useful = only_useful
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left, stats=False):
        board = dict_to_improved_board(percepts)
        action = self.use_strategy(board, player, step, 150, other_params={'heuristic': agent}, stats=stats)
        # print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        return action

if __name__ == "__main__":
    agent = AlphaBetaGeneticAgent()
    agent_main(agent, agent.argument_parser, agent.setup)