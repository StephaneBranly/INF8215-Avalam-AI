

from heuristic.Heuristic import Heuristic
from .NN.neural_network import NN


class NN_Heuristic(Heuristic):
    def __init__(self):
        self.nn = NN([48, 30, 1])
        self.nn.load_best_indiv("./GeneticAgents/NN/gen45_score.json")
        pass

    def evaluate(self, board, player, action=None):
        value = [board.get_percepts()[i][j] for (i,j) in board.get_real_board()]
        return self.nn.predict(value) if player == 1 else 1-self.nn.predict(value)


