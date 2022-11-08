from strategies.MonteCarlo import MonteCarlo
from strategies.simulate_functions import best_score, greedy_play, one_action_heuristic,random_play
from avalam import *
import time

class MonteCarloAgent(EvolvedAgent, MonteCarlo):
    def __init__(self, play_fn=one_action_heuristic, keep_tree=False):
        self.play_fn_name = play_fn.__name__
        self.games = {}
        self.game_time_limit = None
        MonteCarlo.__init__(self, play_fn=play_fn, keep_tree=keep_tree)
        EvolvedAgent.__init__(self)
    
    """A monte carlo agent."""
    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None): 
        if time_left:
            if step in [1,2]:
                self.game_time_limit = time_left
            alpha = 0.00001
            beta = 2/18 - 2*alpha
            cstep = (step - step % 2)/2 + 1
            time_to_play = self.game_time_limit * ((beta - alpha)/(1 - 18) * (cstep - 18) + alpha)
            if time_to_play<=1:
                time_to_play = 1
            
        else:
            time_to_play = 1

        board = dict_to_improved_board(percepts, compute_isolated_towers=False)
        start_time = time.time()
        
        action = self.use_strategy(board, player, step, time_to_play=time_to_play,stats=True)
        
        print(f"Action: {action} for step {step} \t| Time: {time.time() - start_time}\t")
        return action

    def pool_ended(self, pool_results, player, pool_id=None):
        self.games = {}
        return super().pool_ended(pool_results, player, pool_id)

    def get_agent_id(self):
        return f"Monte Carlo Agent | {self.play_fn_name}"

if __name__ == "__main__":
    agent_main(MonteCarloAgent(play_fn=best_score))

