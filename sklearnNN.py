from avalam import ImprovedBoard
from sklearn.neural_network import MLPRegressor
import json

def gen_transposition(state):
    dic = {}
    dic["board"] = [row[::-1] for row in state['board'][::-1]]
    dic["depth"] = state["depth"]
    dic["win"] = state["win"]
    return dic

with open("./states/states.json", 'r') as f:
    states = json.loads(f.read())
    print("nb state ",len(states["states"]))
    nb=len(states["states"])
    for i in range(nb):
        states["states"].append(gen_transposition(states["states"][i]))

states = states["states"]
b = ImprovedBoard()
X = [[state["board"][i][j] for (i,j) in b.get_real_board()]+[state["depth"]+1] for state in states]
Y = [state["win"] for state in states]
X_train = X[:int(len(X)*0.8)]
Y_train = Y[:int(len(Y)*0.8)]
X_test = X[int(len(X)*0.8):]
Y_test = Y[int(len(Y)*0.8):]

regr = MLPRegressor(random_state=1, max_iter=500).fit(X_train, Y_train)
print(regr.score(X_test, Y_test))

