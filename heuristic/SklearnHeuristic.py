import json

from heuristic.Heuristic import Heuristic
from avalam import ImprovedBoard

from sklearn.neural_network import MLPRegressor

class HeuristicSklearn(Heuristic):
    def __init__(self):
        with open("./states/states.json", 'r') as f:
            states = json.loads(f.read())
            print("nb state ",len(states["states"]))
            nb=len(states["states"])
            for i in range(nb):
                states["states"].append(self.gen_transposition(states["states"][i]))
        self.states = states["states"]
        self.regr = MLPRegressor(random_state=1, max_iter=500)
        self.fit()

    def fit(self):
        b = ImprovedBoard()
        X = [[state["board"][i][j] for (i,j) in b.get_real_board()] for state in self.states]
        Y = [state["win"] for state in self.states]

        self.regr.fit(X, Y)

    def gen_transposition(self,state):
        dic = {}
        dic["board"] = [row[::-1] for row in state['board'][::-1]]
        dic["depth"] = state["depth"]
        dic["win"] = state["win"]
        return dic

    def evaluate(self, board, player, action=None):
        value = [board.get_percepts()[i][j] for (i,j) in board.get_real_board()]

        if player == 1:
            return self.regr.predict([value])[0]
        else:
            return 1-self.regr.predict([value])[0]

    def __str__(self):
        return "SklearnHeuristic"