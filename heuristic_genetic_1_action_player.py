from MCTS.observation_function_mcts import *
from avalam import *
from genetic_player import GeneticAgent
from heuristic.heuristic import Genetic_1_action_heuristic, Genetic_single_loop_heuristic
from matplotlib.backends.backend_pdf import PdfPages

from heuristic.stats import generate_dataframes, generate_header_page, plot_param_evolution 
from heuristic.observation_function import finish_tower, isolate_tower, ennemy_isolate_tower, mult_create_tower5, mult_create_tower4, mult_create_tower2, mult_create_tower3, enemy_mult_create_tower2, enemy_mult_create_tower3, enemy_mult_create_tower4, enemy_mult_create_tower5, score_after_action, remaining_actions
class Heuristic1ActionAgent(GeneticAgent):
    def play_agent(self, agent, percepts, player, step, time_left):
        """
        here define the action of your agent
        """
        board = dict_to_improved_board(percepts)
        best_action = ()
        best_score = -99999999

        for action in board.get_actions():
            board.play_action(action)
            current_score = agent.evaluate(board, player)
            board.undo_action()
            if current_score > best_score:
                best_score = current_score
                best_action = action

        return best_action

    def default_agent(self):
        return Genetic_single_loop_heuristic(whole_board_functions=[count_neighbour_size_0, count_neighbour_size_p1, count_neighbour_size_m1, count_neighbour_size_p2, count_neighbour_size_m2, count_neighbour_size_p3, count_neighbour_size_m3, count_neighbour_size_p4, count_neighbour_size_m4, count_neighbour_size_p5, count_neighbour_size_m5])
        # return Genetic_1_action_heuristic(functions=[isolate_tower, ennemy_isolate_tower, mult_create_tower5,mult_create_tower4, mult_create_tower3, mult_create_tower2, enemy_mult_create_tower5, enemy_mult_create_tower4, enemy_mult_create_tower3, enemy_mult_create_tower2,score_after_action, remaining_actions])

    def generate_stats_file(self):
        dfs = generate_dataframes(self.save_path)
        with PdfPages(f"{self.save_path}/stats.pdf") as pdf:
            fig = generate_header_page(self.save_path)
            pdf.savefig(fig)
            for param in range(len(dfs)):
                if len(self.current_agent.interprete_params()) <= param:
                    function_name = None
                else:
                    function_name = self.current_agent.interprete_params()[param]
                fig = plot_param_evolution(dfs, param, function_name)
                pdf.savefig(fig)

if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=-1, help="play : index of indiv if -1 take best | number of indiv per gen", type=int)
        parser.add_argument("-G", "--generation", default=0, help="play : index of gen | train : number of gen", type=int)
        parser.add_argument("-M", "--mode", default="train", help="train | play | evaluate | stats", type=str)
        parser.add_argument("-S","--save", default="NN_heuristic", help="path to save the NN", type=str)
        parser.add_argument("-R","--rate", default=1, help="mutation rate", type=float)
        parser.add_argument("-K","--keep", default=10, help="percentage of agent we keep [0:100]", type=int)
    agent = Heuristic1ActionAgent()
    agent_main(agent, argument_parser, agent.setup)