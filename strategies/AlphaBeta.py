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


        init_board = board.clone()

        max_depth = 4
        heuristic = other_params['heuristic']

        _, m, explored, hash_reduced, transposition = self.max_value(board, init_board, heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play, 0, 0, 0)
        if stats:
            print(f"AlphaBeta hash_reduced {hash_reduced} | transposition {transposition}")
        return m

    def evaluate_state(self, heuristic, init_board, board, action, player):
        board.play_action(action)
        score = heuristic.evaluate(board, player, action)
        board.undo_action()
        return score

    def max_value(self, init_board, current_board, heuristic, player, alpha, beta, depth, max_depth, hash_maps, start, step, time_to_play, explored, hash_reduced, transposition):
        explored += 1

        if depth==max_depth or time.time()-start > time_to_play:
            return (heuristic.evaluate(current_board, player, None),None, explored, hash_reduced, transposition)
        if(step+depth > 20 and len([a for a in current_board.get_actions()])==0):
            return (current_board.get_score()*player*1000,None, explored, hash_reduced, transposition)
        if depth>=1:
            h = hash(tuple(map(tuple, current_board.m)))
            if h in hash_maps[depth]:
                hash_reduced += 1
                return hash_maps[depth][h]
            else :
                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in hash_maps[depth]:
                    
                    transposition += 1
                    return hash_maps[depth][h2]
        else:

            h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
            if h2 in hash_maps[depth]:
                transposition += 1
                return hash_maps[depth][h2]
            
        v = -math.inf
        m = None
        if self.only_useful:
            useful_towers = current_board.get_useful_towers()
            actions = [a for a in current_board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
        else:
            actions = [a for a in current_board.get_actions()]
        actions.sort(key=lambda x: self.evaluate_state(heuristic, init_board, current_board, x, player), reverse=True)
        for a in actions:
            current_board.play_action(a)
            nV, _, dexplored, dhash_reduced, dtransposition = self.min_value(init_board, current_board, heuristic, player, alpha, beta, depth+1, max_depth, hash_maps, start, step, time_to_play, explored, hash_reduced, transposition)
            explored += dexplored
            hash_reduced += dhash_reduced
            transposition += dtransposition
            current_board.undo_action()
            if nV > v:
                v = nV
                m = a
                alpha = max(alpha, v)
            if v >= beta:
                return (v,m, explored, hash_reduced, transposition)
        if len(hash_maps[depth])<100000:
            if depth==0:
                h = hash(tuple(map(tuple, current_board.m)))
            hash_maps[depth][h] = (v,m, explored, hash_reduced, transposition)
        return (v,m, explored, hash_reduced, transposition)
    
    def min_value(self, init_board, current_board, heuristic, player, alpha, beta, depth, max_depth, hash_maps, start, step, time_to_play, explored, hash_reduced, transposition):
        explored += 1
        if depth==max_depth or time.time()-start > time_to_play:
            return (heuristic.evaluate(current_board, player, None),None, explored, hash_reduced, transposition)
        if(step+depth > 20 and len([a for a in current_board.get_actions()])==0):
            return (current_board.get_score()*player*1000,None, explored, hash_reduced, transposition)
        if depth>=1:
            h = hash(tuple(map(tuple, current_board.m)))
            if h in hash_maps[depth]:
                hash_reduced += 1
                return hash_maps[depth][h]
            else :
                h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
                if h2 in hash_maps[depth]:
                    transposition += 1
                    return hash_maps[depth][h2]
        else:
            h2 = hash(tuple(map(lambda e : tuple(reversed(e)) , reversed(current_board.m))))
            if h2 in hash_maps[depth]:
                transposition += 1
                return hash_maps[depth][h2]
        v = math.inf
        m = None
        if self.only_useful:
            useful_towers = current_board.get_useful_towers()
            actions = [a for a in current_board.get_actions() if (a[0],a[1]) in useful_towers or (a[2],a[3]) in useful_towers]
        else:
            actions = [a for a in current_board.get_actions()]
        actions.sort(key=lambda x: self.evaluate_state(heuristic, init_board, current_board, x, player), reverse=False)
        for a in actions:
            current_board.play_action(a)
            nV, _, dexplored, dhash_reduced, dtransposition = self.max_value(init_board, current_board, heuristic, player, alpha, beta, depth+1, max_depth, hash_maps, start, step, time_to_play, explored, hash_reduced, transposition)
            explored += dexplored
            hash_reduced += dhash_reduced
            transposition += dtransposition
            current_board.undo_action()
            if nV < v:
                v = nV
                m = a
                beta = min(beta, v)
            if alpha >= v:
                return (v,m, explored, hash_reduced, transposition)
        if len(hash_maps[depth])<100000:
            if depth==0:
                h = hash(tuple(map(tuple, current_board.m)))
            hash_maps[depth][h] = (v,m, explored, hash_reduced, transposition)
        return (v,m, explored, hash_reduced, transposition)

