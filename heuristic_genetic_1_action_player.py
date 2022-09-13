from avalam import *
from genetic_player import GeneticAgent
from heuristic.heuristic import Genetic_1_action_heuristique


class Heuristic1ActionAgent(GeneticAgent):

    def play_agent(self, agent,percepts, player, step, time_left):
        """
        here define the action of your agent
        """
        board = dict_to_board(percepts)
        best_action = ()
        best_score = -99999999


        for action in board.get_actions():
            current_score = agent.evaluate(board, player, action)
            if current_score > best_score:

                best_score = current_score
                best_action = action

        return best_action

    def default_agent(self):
        return Genetic_1_action_heuristique()


if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=-1, help="play : index of indiv if -1 take best | number of indiv per gen", type=int)
        parser.add_argument("-G", "--generation", default=0, help="play : index of gen | train : number of gen", type=int)
        parser.add_argument("-M", "--mode", default="train", help="train | play | evaluate", type=str)
        parser.add_argument("-S","--save", default="NN_heuristic", help="path to save the NN", type=str)
        parser.add_argument("-R","--rate", default=0.01, help="mutation rate", type=float)
        parser.add_argument("-K","--keep", default=10, help="percentage of agent we keep [0:100]", type=int)
    agent = Heuristic1ActionAgent()
    agent_main(agent, argument_parser, agent.setup)