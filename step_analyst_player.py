from avalam import *
from greedy_player import GreedyAgent

class StepAnalystPlayer(EvolvedAgent):
    def __init__(self, agent=GreedyAgent(1)):
        self.agent = agent
        self.step_analysed = 0
        self.player_1_step = False

    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        if step == 1:
            self.player_1_step = True

        if step == self.step_analysed:
            # here we take the worst action for player, means the best for the opponent
            return self.agent.play(percepts, -player, step, time_left, game_id, pool_id)
        else:
            return self.agent.play(percepts, player, step, time_left, game_id, pool_id)
        
    def pool_ended(self, pool_results, player, pool_id=None):
        self.step_analysed += 1
        return super().pool_ended(pool_results, player, pool_id)

    def get_agent_id(self):
        return f"Step Analyst Player {self.step_analysed} | {self.player_1_step}"