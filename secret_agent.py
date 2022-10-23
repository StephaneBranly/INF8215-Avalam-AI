from avalam import *
import time

from best_move_genetic_agent import BestMoveGeneticAgent
from monte_carlo_player import MonteCarloAgent
from alpha_beta_genetic_agent_IDS import AlphaBetaIDSGeneticAgent
from strategies.simulate_functions import one_action_heuristic

class SecretAgent(EvolvedAgent):
    def __init__(self):
        self.total_time_to_play = 0

        # Agent 1
        agent1 = BestMoveGeneticAgent()
        agent1.setup(
            None,
            None, 
            {
                'mode': "evaluate",
                'save': "fullObsInit",
                'generation': 40
            }
        )
        # Agent 2
        agent2 = AlphaBetaIDSGeneticAgent(only_useful=True, max_step=2)
        agent2.setup(
            None,
            None, 
            {
                'mode': "evaluate",
                'save': "fullObsInit",
                'generation': 40
            }
        )
        # Agent 3
        agent3 = MonteCarloAgent(play_fn=one_action_heuristic)
        # Agent 4
        agent4 = AlphaBetaIDSGeneticAgent(only_useful=True, max_step=10)
        agent4.setup(
            None,
            None, 
            {
                'mode': "evaluate",
                'save': "fullObsInit",
                'generation': 40
            }
        )

        self.agents = [agent1, agent2, agent3, agent4]
        self.step_limits = [8, 12, 27, 40]
        self.time_to_play = [0,0,0,0]
        super().__init__()

    def hasEvolded(self):
        return super().hasEvolded()

    """A dumb random agent."""
    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        if step in [1,2]:
            self.total_time_to_play = time_left
            self.time_to_play = [
                60,
                60,
                60,
                60
            ]
        
        agent_to_play = None
        time_to_play = None
        for i in range(len(self.step_limits)):
            if step <= self.step_limits[i]:
                agent_to_play = self.agents[i]
                time_to_play = time_left / ((35-step)/2)
                if time_to_play < 0:
                    time_to_play = 1
                break
        start = time.time()
        board = dict_to_improved_board(percepts)
        if i == 0:
            action = agent_to_play.use_strategy(board.clone(), player, step, other_params={'heuristic': agent_to_play.current_heuristic}, time_to_play=time_to_play)
        elif i == 2:
            action = agent_to_play.use_strategy(board.clone(), player, step, time_to_play=time_to_play)
        else:
            action = agent_to_play.use_strategy(board.clone(), player, step,
            other_params={
                'heuristic': agent_to_play.current_heuristic,
                'max_step': agent_to_play.max_step
            }, time_to_play=time_to_play)
        print(f"Agent {i} ({agent_to_play.__class__.__name__})\t\t| played {action}\t\t| step {step}\t\t| in {time.time()-start}s")
        return action

    def get_agent_id(self):
        return "Secret Agent"

if __name__ == "__main__":
    agent_main(SecretAgent())
