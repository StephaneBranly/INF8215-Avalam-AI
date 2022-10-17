import math
import time
from heuristic.GeneticSingleLoop import GeneticSingleLoop
from avalam import *
from genetic_player import GeneticAgent
from heuristic.Heuristic import *
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

from heuristic.stats import generate_dataframes, generate_header_page, plot_param_evolution 

class Heuristic2ActionAgent(GeneticAgent):

    def __init__(self,only_useful = False) -> None:
        self.explored = 0
        self.only_useful = only_useful
        super().__init__()

    def get_agent_id(self):
        return super().get_agent_id() + f"_{self.only_useful}"    

    def play_agent(self, agent, percepts, player, step, time_left):

        """a = [(5,0,4,1),(4,1,4,0),(0,3,1,2),(1,2,1,1),(1,4,2,3),(2,3,2,4),(2,1,3,2),(3,2,2,2),(8,5,7,4),(7,4,7,5),(2,5,3,4),(0,2,1,3),(3,4,4,3),(2,6,3,7),(3,7,3,8),(4,8,5,7),(5,7,6,7),(8,6,7,7),(1,3,2,2),(3,3,4,2),(4,2,5,2),(7,7,6,6),(4,7,5,6),(5,6,5,5),(7,6,6,5),(6,5,6,4),(4,5,3,6),(3,6,4,6),(6,2,6,3),(4,0,3,1)]
        if step<=len(a):
            return a[step-1]"""
        explored = 0

        start = time.time()


        HashMaps = []
        for i in range(0, 40):
            HashMaps.append({})

        hashReduced = 0
        transposition = 0

        def lambda_x(agent, init_board, board, x, player):
            board.play_action(x)
            score = agent.evaluate(board, player)
            board.undo_action()
            return score


        def max_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal explored
            nonlocal start
            nonlocal step
            nonlocal HashMaps
            nonlocal hashReduced
            nonlocal transposition
            explored += 1


            if depth==max_depth or time.time()-start > 10:
                return (agent.evaluate(current_board, player),None)
            if(step+depth > 20 and len([a for a in current_board.get_actions()])==0):
                return (current_board.get_score()*player*1000,None)
            if depth>=1:
                h = hash(tuple(map(tuple, current_board.m)))
                if h in HashMaps[depth]:
                    hashReduced += 1
                    return HashMaps[depth][h]
                else :
                    h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                    if h2 in HashMaps[depth]:
                        
                        transposition += 1
                        return HashMaps[depth][h2]
            else:

                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in HashMaps[depth]:
                    transposition += 1
                    return HashMaps[depth][h2]
                
            v = -math.inf
            m = None
            if self.only_useful:
                useful_towers = current_board.get_useful_towers()
                actions = [a for a in current_board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
            else:
                actions = [a for a in current_board.get_actions()]
            actions.sort(key=lambda x: lambda_x(agent, init_board, current_board, x, player), reverse=True)
            for a in actions:
                current_board.play_action(a)
                nV = min_value(init_board, current_board, agent, player, alpha, beta, depth+1, max_depth)[0]
                current_board.undo_action()
                if(nV > v):
                    v = nV
                    m = a
                    alpha = max(alpha, v)
                if(v >= beta):
                    return (v,m)
            if len(HashMaps[depth])<100000:
                if depth==0:
                    h = hash(tuple(map(tuple, current_board.m)))
                HashMaps[depth][h] = (v,m)
            return (v,m)
        
        def min_value(init_board, current_board, agent, player, alpha, beta, depth, max_depth):
            nonlocal start
            nonlocal explored
            nonlocal step
            nonlocal HashMaps
            nonlocal hashReduced
            nonlocal transposition
            explored += 1
            if depth==max_depth or time.time()-start > 10:
                return (agent.evaluate(current_board, player),None)
            if(step+depth > 20 and len([a for a in current_board.get_actions()])==0):
                
                return (current_board.get_score()*player*1000,None)
            if depth>=1:
                    h = hash(tuple(map(tuple, current_board.m)))
                    if h in HashMaps[depth]:
                        hashReduced += 1
                        return HashMaps[depth][h]
                    else :
                        h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                        if h2 in HashMaps[depth]:
                            transposition += 1
                            return HashMaps[depth][h2]
            else:
                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in HashMaps[depth]:
                    transposition += 1
                    return HashMaps[depth][h2]
            v = math.inf
            m = None
            if self.only_useful:
                useful_towers = current_board.get_useful_towers()
                actions = [a for a in current_board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
            else:
                actions = [a for a in current_board.get_actions()]
            actions.sort(key=lambda x: lambda_x(agent, init_board, current_board, x, player), reverse=False)
            for a in actions:
                current_board.play_action(a)
                nV = max_value(init_board, current_board, agent, player, alpha, beta, depth+1, max_depth)[0]
                current_board.undo_action()
                if(nV < v):
                    v = nV
                    m = a
                    beta = min(beta, v)
                if(alpha >= v):
                    return (v,m)
            if len(HashMaps[depth])<100000:
                if depth==0:
                    h = hash(tuple(map(tuple, current_board.m)))
                HashMaps[depth][h] = (v,m)
            return (v,m)
    

        board = dict_to_improved_board(percepts)
        init_board = dict_to_improved_board(percepts)

        max_depth = 4
        

        v , m = max_value(board, init_board, agent, player, -math.inf, math.inf, 0, max_depth)
        print("step", step,"explored", explored,"time",time.time()-start,"hashReduced",hashReduced,"transposition",transposition)

        return m

    def generate_stats_file(self):
        dfs = generate_dataframes(self.save_path)
        with PdfPages(f"{self.save_path}/stats.pdf") as pdf:
            fig = generate_header_page(self.save_path)
            pdf.savefig(fig)
            for param in range(len(dfs)):
                if len(self.default_heuristic().interprete_params()) <= param:
                    function_name = None
                else:
                    function_name = self.default_heuristic().interprete_params()[param]
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