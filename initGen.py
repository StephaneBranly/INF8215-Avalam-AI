import random
from heuristic.observation_function import *
from heuristic.GeneticSingleLoop import GeneticSingleLoop


save = "fullObsInit"
heuristic = GeneticSingleLoop()
size = 30

functions = [single_loop_isolated_tower,enemy_single_loop_isolated_tower,single_loop_tower5,single_loop_tower4,single_loop_tower3,single_loop_tower2,enemy_single_loop_tower5,enemy_single_loop_tower4,enemy_single_loop_tower3,enemy_single_loop_tower2,single_loop_isolated_tower5,single_loop_isolated_tower4,single_loop_isolated_tower3,single_loop_isolated_tower2,enemy_single_loop_isolated_tower5,enemy_single_loop_isolated_tower4,enemy_single_loop_isolated_tower3,enemy_single_loop_isolated_tower2,wineable_tower,enemy_wineable_tower,score,remaining_actions]

def positivRandom():
    return random.uniform(0,1)

def negativRandom():
    return random.uniform(-1,0)

def fullRandom():
    return random.uniform(-1,1)

for i in range(size):
    indiv = heuristic.clone()
    parameters = []
    # isolated tower
    parameters.append(positivRandom())
    # enemy isolated tower
    parameters.append(negativRandom())
    # tower 5
    parameters.append(positivRandom())
    # tower 4
    parameters.append(negativRandom())
    # tower 3
    parameters.append(positivRandom())
    # tower 2
    parameters.append(negativRandom())
    # enemy tower 5
    parameters.append(negativRandom())
    # enemy tower 4
    parameters.append(positivRandom())
    # enemy tower 3
    parameters.append(negativRandom())
    # enemy tower 2
    parameters.append(positivRandom())
    # isolated tower 5
    parameters.append(positivRandom())
    # isolated tower 4
    parameters.append(positivRandom())
    # isolated tower 3
    parameters.append(positivRandom())
    # isolated tower 2
    parameters.append(positivRandom())
    # enemy isolated tower 5
    parameters.append(negativRandom())
    # enemy isolated tower 4
    parameters.append(negativRandom())
    # enemy isolated tower 3
    parameters.append(negativRandom())
    # enemy isolated tower 2
    parameters.append(negativRandom())
    # wineable tower
    parameters.append(positivRandom())
    # enemy wineable tower
    parameters.append(negativRandom())
    # score
    parameters.append(positivRandom())
    # remaining actions
    parameters.append(fullRandom())

    indiv.set_parameters(parameters)
    indiv.set_functions(functions)
    indiv.save_as_json(f"GeneticAgents/{save}/gen0.json",0)

