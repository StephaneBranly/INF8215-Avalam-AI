from strategies.Strategy import Strategy
import time
import math

class AlphaBeta(Strategy):
    def __init__(self, only_useful=False):
        self.only_useful = only_useful
        super().__init__()

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):

        start = time.time()

        hashMaps = []
        for i in range(0, 40):
            hashMaps.append({})


        max_depth = 3

        heuristic = other_params['heuristic']

        _, m, explored, hash_reduced, transposition = self.max_value(board, heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play)

        print(f"AlphaBeta, Step {step} | hash_reduced {hash_reduced} | transposition {transposition} | explored {explored} | time {time.time()-start}")

        return m

    def evaluate_state(self, heuristic, board, action, player):
        board.play_action(action)
        score = heuristic.evaluate(board, player, action)
        board.undo_action()
        return score

    def check_already_visited(self, board, depth, hash_maps):

        # etats deja vus
        if depth >= 1:
            h = hash(tuple(map(tuple, board.m)))
            if h in hash_maps[depth]:
                #print("hashReduced")
                return (hash_maps[depth][h][0],hash_maps[depth][h][1],1,1,0)
        
        # transposition
        h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(board.m))))
        if h2 in hash_maps[depth]:
            #print("transposition")
            return (hash_maps[depth][h2][0],hash_maps[depth][h2][1],1,0,1)

        return None

    def max_value(self, board, heuristic, player, alpha, beta, depth, max_depth, hash_maps, start, step, time_to_play):

        # temp ecoulé ou prof max atteinte
        if depth==max_depth or time.time()-start > time_to_play:
            v = heuristic.evaluate(board, player, None)
            h = hash(tuple(map(tuple, board.m)))
            hash_maps[depth][h] = (v,None) 
            #print("max depth")
            return (v,None, 1, 0, 0)
        
        # fin de partie
        if(board.is_finished()):
            v = board.get_score()*player*1000
            h = hash(tuple(map(tuple, board.m)))
            hash_maps[depth][h] = (v,None) 
            #print("fin de partie")
            return (v,None, 1, 0, 0)

        alreadyVisited = self.check_already_visited(board, depth, hash_maps)
        if alreadyVisited is not None:
            return alreadyVisited
        
        v = -math.inf
        m = None

        if self.only_useful:
            useful_towers = board.get_useful_towers()
            actions = [a for a in board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
        else:
            actions = [a for a in board.get_actions()]
        
        actions.sort(key=lambda x: self.evaluate_state(heuristic, board, x, player), reverse=True)
        explored = 1
        hash_reduced = 0
        transposition = 0

        for a in actions:
            board.play_action(a)
            nV, _, dexplored, dhash_reduced, dtransposition = self.min_value(board, heuristic, player, alpha, beta, depth+1, max_depth, hash_maps, start, step, time_to_play)
            explored += dexplored
            hash_reduced += dhash_reduced
            transposition += dtransposition
            board.undo_action()
            if nV > v:
                v = nV
                m = a
                alpha = max(alpha, v)
            if v >= beta:
                #print("beta cut")
                return (v,m, explored, hash_reduced, transposition)
        # memorisation
        if len(hash_maps[depth])<100000:
            h = hash(tuple(map(tuple, board.m)))
            hash_maps[depth][h] = (v,m)
        #print("all actions explored")
        return (v,m, explored, hash_reduced, transposition)
    
    def min_value(self, board, heuristic, player, alpha, beta, depth, max_depth, hash_maps, start, step, time_to_play):
        
        # temp ecoulé ou prof max atteinte
        if depth==max_depth or time.time()-start > time_to_play:
            #print("max depth")
            return (heuristic.evaluate(board, player, None),None, 1, 0, 0)

        # fin de partie
        if(board.is_finished()):
            #print("fin de partie")
            return (board.get_score()*player*1000,None, 1, 0, 0)

        alreadyVisited = self.check_already_visited(board, depth, hash_maps)
        if alreadyVisited is not None:
            return alreadyVisited

        v = math.inf
        m = None

        if self.only_useful:
            useful_towers = board.get_useful_towers()
            actions = [a for a in board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
        else:
            actions = [a for a in board.get_actions()]

        actions.sort(key=lambda x: self.evaluate_state(heuristic, board, x, player), reverse=False)
        explored = 1
        hash_reduced = 0
        transposition = 0
        for a in actions:
            board.play_action(a)
            nV, _, dexplored, dhash_reduced, dtransposition = self.max_value(board, heuristic, player, alpha, beta, depth+1, max_depth, hash_maps, start, step, time_to_play)
            explored += dexplored
            hash_reduced += dhash_reduced
            transposition += dtransposition
            board.undo_action()
            if nV < v:
                v = nV
                m = a
                beta = min(beta, v)
            if alpha >= v:
                #print("alpha cut")
                return (v,m, explored, hash_reduced, transposition)

        # memorisation
        if len(hash_maps[depth])<100000:
            h = hash(tuple(map(tuple, board.m)))
            hash_maps[depth][h] = (v,m)
        #print("all actions explored")
        return (v,m, explored, hash_reduced, transposition)

