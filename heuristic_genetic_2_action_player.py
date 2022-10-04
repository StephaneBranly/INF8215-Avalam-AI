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

        HashMaps = []
        for i in range(0, 10):
            HashMaps.append({})

        hashReduced = 0
        transposition = 0
        max_depth_reached = 0

        def max_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal explored
            nonlocal start
            nonlocal step
            nonlocal HashMaps
            nonlocal hashReduced
            nonlocal transposition
            explored += 1

            if depth==max_depth or time.time()-start > 600:
                return (agent.evaluate(current_board, player),None)
            if(step+depth < 20 and current_board.get_actions()==[]):
                return (current_board.get_score()*player*1000,None)
            if depth>=1:
                h = hash(tuple(map(tuple, current_board.m)))
                if h in HashMaps[step]:
                    hashReduced += 1
                    return HashMaps[step][h]
                else :
                    h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                    if h2 in HashMaps[step]:
                        
                        transposition += 1
                        return HashMaps[step][h2]
            else:

                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in HashMaps[step]:
                    transposition += 1
                    return HashMaps[step][h2]
                
            v = -math.inf
            m = None
            actions = [a for a in current_board.get_actions()]
            #actions.sort(key=lambda x: current_board.clone().play_action(x).get_score()*player, reverse=True)
            actions.sort(key=lambda x: agent.evaluate(current_board.clone().play_action(x), player), reverse=True)
            for a in actions:
                nV = min_value(init_board, current_board.clone().play_action(a), agent, player, alpha, beta, depth+1, max_depth)[0]
                if(nV > v):
                    v = nV
                    m = a
                    alpha = max(alpha, v)
                if(alpha >= beta):
                    return (v,m)
            if len(HashMaps[step])<100000:
                if depth==0:
                    h = hash(tuple(map(tuple, current_board.m)))
                HashMaps[step][h] = (v,m)
            return (v,m)
        
        def min_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal start
            nonlocal explored
            nonlocal step
            nonlocal HashMaps
            nonlocal hashReduced
            nonlocal transposition
            explored += 1
            if depth==max_depth or time.time()-start > 600:
                return (agent.evaluate(current_board, player),None)
            if(step+depth < 20 and current_board.get_actions()==[]):
                return (current_board.get_score()*player*1000,None)
            if depth>=1:
                    h = hash(tuple(map(tuple, current_board.m)))
                    if h in HashMaps[step]:
                        hashReduced += 1
                        return HashMaps[step][h]
                    else :
                        h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                        if h2 in HashMaps[step]:
                            transposition += 1
                            return HashMaps[step][h2]
            else:
                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in HashMaps[step]:
                    transposition += 1
                    return HashMaps[step][h2]
            v = math.inf
            m = None
            actions = [a for a in current_board.get_actions()]
            #actions.sort(key=lambda x: current_board.clone().play_action(x).get_score()*player, reverse=False)
            actions.sort(key=lambda x: agent.evaluate(current_board.clone().play_action(x), player), reverse=False)
            for a in actions:

                nV = max_value(init_board, current_board.clone().play_action(a), agent, player, alpha, beta, depth+1, max_depth)[0]

                if(nV < v):
                    v = nV
                    m = a
                    beta = min(beta, v)
                if(alpha >= beta):
                    return (v,m)
            if len(HashMaps[step])<100000:
                if depth==0:
                    h = hash(tuple(map(tuple, current_board.m)))
                HashMaps[step][h] = (v,m)
            return (v,m)
    
        board = dict_to_board(percepts)
        max_depth = 3

        v , m = max_value(board, board, agent, player, -math.inf, math.inf, 0, max_depth)
        print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)
        return m


    def default_agent(self):
        return Genetic_single_loop_heuristic()

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