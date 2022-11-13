from avalam import *
from genetic_player import GeneticAgent
from heuristic.Heuristic import *
from strategies.AlphaBetaIDS import AlphaBetaIDS

class AlphaBetaIDSGeneticAgent(GeneticAgent, AlphaBetaIDS):

    def __init__(self, only_useful = False, max_step=20):
        self.explored = 0
        self.only_useful = only_useful
        self.max_step=max_step
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left, stats=False):

        """if step<=16:
            self.max_step = 1
        elif step<=22:
            self.max_step = 4
        elif step<=24:
            self.max_step = 6"""

        board = dict_to_improved_board(percepts)
        if time_left:
            time_to_play = (time_left/((30-step)/2))-4 if step < 30 else time_left/4
            print("Time to play: ", time_to_play)
        action = self.use_strategy(board, player, step, 6000000 if time_left == None else time_to_play, other_params={'heuristic': agent, 'max_step': self.max_step}, stats=stats)
        # print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        return action

if __name__ == "__main__":
    agent = AlphaBetaIDSGeneticAgent()
    agent_main(agent, agent.argument_parser, agent.setup)