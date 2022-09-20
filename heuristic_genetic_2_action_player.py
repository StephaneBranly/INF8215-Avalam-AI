from heuristic.observation_function import finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2
from avalam import *
from genetic_player import GeneticAgent
from heuristic.heuristic import Genetic_1_action_heuristique
from matplotlib.backends.backend_pdf import PdfPages

from heuristic.stats import generate_dataframes, generate_header_page, plot_param_evolution 

class Heuristic2ActionAgent(GeneticAgent):

    def __init__(self) -> None:
        self.adv_heuristic = self.adv_heuristic = Genetic_1_action_heuristique(functions=[finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2], parameters=[-0.2721167795584365, 0.4606782408928063, -0.3147674027759, 0.8563962271522858, -0.2560162921722944, -0.9818495061249783, 0.0776478812729462, -1.0012428754793652])
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left):
        """
        here define the action of your agent
        """

        board = dict_to_board(percepts)
        means = []

        for action in board.get_actions():

            n_board = board.clone()
            n_board.play_action(action)
            actions_adv = []
 
            for action_adv in n_board.get_actions():

                actions_adv.append((self.adv_heuristic.evaluate(n_board, -player, action_adv),action_adv))

            actions_adv.sort(key=lambda x: x[0], reverse=True)
            actions_adv = actions_adv[:len(actions_adv)//3]
            
            scores = []

            for action_adv in actions_adv:

                n_board = board.clone()
                n_board.play_action(action)
                n_board.play_action(action_adv[1])
                for action2 in n_board.get_actions():
                    #print("action2 :", action2)
                    current_score = agent.evaluate(n_board, player, action2)
                    scores.append(current_score)
            means.append((sum(scores)/len(scores), action))
            
        means.sort(key=lambda x: x[0], reverse=True)

        return means[0][1]

    def default_agent(self):
        return Genetic_1_action_heuristique()

    def generate_stats_file(self):
        dfs = generate_dataframes(self.save_path)
        with PdfPages(f"{self.save_path}/stats.pdf") as pdf:
            fig = generate_header_page(self.save_path)
            pdf.savefig(fig)
            for param in range(len(dfs)):
                if len(self.default_agent().interprete_params()) <= param:
                    function_name = None
                else:
                    function_name = self.default_agent().interprete_params()[param]
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
    agent = Heuristic2ActionAgent()
    agent_main(agent, argument_parser, agent.setup)