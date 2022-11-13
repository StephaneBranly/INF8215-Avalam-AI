import math
from avalam import ImprovedBoard
from heuristic.NN.neural_network import NN
import json
import random

def score(NN,states):
    score = 0
    b = ImprovedBoard()
    for state in states:
        value = [state["board"][i][j] for (i,j) in b.get_real_board()]+[state["depth"]+1]
        score += abs(state["win"] - NN.predict(value))
    return score

def init_empty_gen_file(save,gen):
    with open(save+"/gen"+str(gen)+".json", 'w') as f:
        f.write("{\"gen\":[]}")

def gen_transposition(state):
    dic = {}
    dic["board"] = [row[::-1] for row in state['board'][::-1]]
    dic["depth"] = state["depth"]
    dic["win"] = state["win"]
    return dic

def train(nb_indiv,nb_gens,keep, save):

    init_empty_gen_file(save,0)

    for i in range(nb_indiv):
        nn = NN([49,30,30, 1], "NN"+str(i))
        nn.save_as_json(save+"/gen0.json",0)

    with open("./states/states.json", 'r') as f:
        states = json.loads(f.read())
        print("nb state ",len(states["states"]))
        nb=len(states["states"])
        for i in range(nb):
            states["states"].append(gen_transposition(states["states"][i]))

    states = states["states"]
    training_size = len(states)
    print("Training size : ", training_size)

    for i in range(nb_gens):


        NNs = []
        for j in range(nb_indiv):
            nn = NN([49, 30,30,1])
            nn.load_from_json(save+"/gen"+str(i)+".json",j)
            NNs.append(nn)

        init_empty_gen_file(save,str(i)+"_score")
        scores = {}
        best = math.inf
        for nn in NNs:
            s = score(nn,states)[0]
            if s < best:
                best = s
            scores[nn.name] = s
            nn.save_as_json(save+"/gen"+str(i)+"_score.json",s)

        

        NNs = sorted(NNs, key=lambda x: scores[x.name])

        init_empty_gen_file(save,str(i+1))

        for j in range(nb_indiv//2):
            father = NNs[random.randint(0, nb_indiv*keep//100)]
            mother = NNs[random.randint(0, nb_indiv*keep//100)]
            
            c1,c2 = father.crossover(mother)
            c1.name = "NN"+str(j*2)
            c2.name = "NN"+str(j*2+1)
            c1.mutate()
            c2.mutate()
            c1.save_as_json(save+"/gen"+str(i+1)+".json",0)
            c2.save_as_json(save+"/gen"+str(i+1)+".json",0)


        print("Generation "+str(i)+" done best",best,"median",best/training_size*100,"%")

if __name__ == "__main__":
    train(200,500,10,"./GeneticAgents/NN2")

