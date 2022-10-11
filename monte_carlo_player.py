from MCTS.MonteCarlo import MonteCarlo
from MCTS.simulate_functions import greedy_play
from avalam import *
import time

class MonteCarloAgent(EvolvedAgent, MonteCarlo):
    def __init__(self):
        self.games = {}
        self.time_to_play = None
        self.step_time_to_play = [0.0,0.09799554565701558,0.10192195690157249,0.006124721603563479,0.0861968549796156,0.102728285077951,0.10745486313337216,0.08658129175946548,0.07629586488060569,0.04315144766146994,0.07542224810716365,0.03814031180400891,0.06086196854979614,0.08324053452115812,0.07920792079207921,0.06876391982182628,0.058823529411764684,0.07488864142538976,0.008736167734420491,0.004454342984409803,0.049213744903902144,0.07711581291759464,0.05241700640652301,0.01503340757238307,0.02242283051834597,0.07461024498886415,0.046010483401281305,0.07321826280623607,0.02853814793244029,0.06570155902004453,0.0378567268491555,0.005011135857461028,0.03581828771112405,0.0626391982182628,0.033488642981945246,0.012806236080178168,0.03523587652882935,0.006124721603563479,0.004076878276062888,0.0016703786191536762]
        MonteCarlo.__init__(self, play_fn=greedy_play)
        EvolvedAgent.__init__(self)
    
    """A monte carlo agent."""
    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None): 
        if step in [1,2]:
            self.time_to_play = time_left
            time_to_play = -3
        else:
            time_to_play = 0
        time_to_play += self.step_time_to_play[step] * self.time_to_play
        
        board = dict_to_improved_board(percepts)
        start_time = time.time()

        if game_id not in self.games:
            # case of first turn, we need to initialize the tree
            self.games[game_id] = {
                "board": board,
                "tree": self.node_dict(player=player),
                # "tree": self.load_tree()
            }
            # if step==2:
            #     # if we play second, we need to play the first action in the tree to have the right tree
            #     new_tree, _ = self.go_down_tree(self.games[game_id]["tree"], ImprovedBoard(), board)
            #     self.games[game_id]['tree'] = new_tree
        else:        
            new_tree, action_made = self.go_down_tree(self.games[game_id]["tree"], self.games[game_id]["board"], board)
            # print(f"\tOpponent has player action {action_made}\t| Saved {new_tree['n']} iterations")
            self.games[game_id]['tree'] = new_tree

        self.games[game_id]['tree']['action_made'] = None

        # We compute the time we have to play
        # if pool_id % 2 == 0:
        #     time_to_play = self.time_to_play / 17
        # else:

        action, iterations, new_tree, new_board = self.mcts(board, player, step, time_limit=time_to_play, tree=self.games[game_id]['tree'])
        self.games[game_id]['tree'] = new_tree
        self.games[game_id]['board'] = new_board
        print(f"Time left: {time_left-time.time() + start_time}\t| Action: {action} for step {step} \t| Time: {time.time() - start_time}\t| Iterations: {iterations}")
        return action

    def pool_ended(self, pool_results, player, pool_id=None):
        self.games = {}
        return super().pool_ended(pool_results, player, pool_id)

    def get_agent_id(self):
        return "Monte Carlo Agent"

if __name__ == "__main__":
    agent_main(MonteCarloAgent())

