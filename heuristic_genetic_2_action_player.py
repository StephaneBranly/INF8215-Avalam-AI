import math
import time
from heuristic.observation_function import finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2
from avalam import *
from genetic_player import GeneticAgent
from heuristic.heuristic import *
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

from heuristic.stats import generate_dataframes, generate_header_page, plot_param_evolution 

class Heuristic2ActionAgent(GeneticAgent):

    def __init__(self) -> None:
        self.explored = 0
        super().__init__()

    def play_agent(self, agent, percepts, player, step, time_left):

        explored = 0

        start = time.time()

        def max_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal explored
            nonlocal start
            nonlocal step
            explored += 1
            if time.time()-start > 30:
                #print("stop",time.time()-start)
                return (agent.evaluate(init_board, current_board, player,None),None)
            if(step+depth < 20 and current_board.get_actions()==[]):
                return (current_board.get_score()*player*1000,None)
            v = -math.inf
            m = None
            actions = [a for a in current_board.get_actions()]
            actions.sort(key=lambda x: agent.evaluate(init_board, current_board.clone().play_action(x), player,x), reverse=True)
            for a in actions:
                nV = min_value(init_board, current_board.clone().play_action(a), agent, player, alpha, beta, depth+1, max_depth)[0]
                if(nV > v):
                    v = nV
                    m = a
                    alpha = max(alpha, v)
                if(alpha >= beta):
                    return (v,m)
            return (v,m)
        
        def min_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal start
            nonlocal explored
            nonlocal step
            explored += 1
            if time.time()-start > 30:
                #print("stop",time.time()-start)
                return (agent.evaluate(init_board, current_board, player,None),None)
            if(step+depth < 20 and current_board.get_actions()==[]):
                return (current_board.get_score()*player*1000,None)
            v = math.inf
            m = None
            actions = [a for a in current_board.get_actions()]
            actions.sort(key=lambda x: agent.evaluate(init_board, current_board.clone().play_action(x), player,x), reverse=False)
            for a in actions:
            #for a in current_board.get_actions():
                nV = max_value(init_board, current_board.clone().play_action(a), agent, player, alpha, beta, depth+1, max_depth)[0]
                if(nV < v):
                    v = nV
                    m = a
                    beta = min(beta, v)
                if(alpha >= beta):
                    return (v,m)
            return (v,m)
    
        board = dict_to_board(percepts)
        max_depth = 30
        size = len([a for a in board.get_actions()])
        """while pow(size,max_depth) > 1000000:
            max_depth -= 1"""

        v , m = max_value(board, board, agent, player, -math.inf, math.inf, 0, max_depth)
        print("time",time.time()-start)
        print("step", step,"explored", explored)
        return m


    def default_agent(self):
        return Genetic_mult_actions_heuristique()

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