import random
from heuristic.observation_function import *
from heuristic.GeneticSingleLoop import GeneticSingleLoop


save = "DoubleHeuristicMaxState"
heuristic = GeneticSingleLoop()
size = 41

functions = [
    single_loop_isolated_tower,
    enemy_single_loop_isolated_tower,
    single_loop_tower5,
    single_loop_tower4,
    single_loop_tower3,
    single_loop_tower2,
    enemy_single_loop_tower5,
    enemy_single_loop_tower4,
    enemy_single_loop_tower3,
    enemy_single_loop_tower2,
    single_loop_isolated_tower4,
    single_loop_isolated_tower3,
    single_loop_isolated_tower2,
    single_loop_isolated_tower1,
    enemy_single_loop_isolated_tower4,
    enemy_single_loop_isolated_tower3,
    enemy_single_loop_isolated_tower2,
    enemy_single_loop_isolated_tower1,
    moveable_tower,
    enemy_moveable_tower,
    wineable_tower,
    enemy_wineable_tower,
    score
    ]

parameters = [-0.7, -0.6, 0, -1, -0.19617099525940007, -0.4723650485169191, -0.35238542794390293, 0.21886513659756623, -0.5223017253073303, 0.9545302935971265, 0.4401817690594282, 0.8220606383061779, 0.1310969888769502, 0.6228291752399198, -0.4640505977588232, -0.6144121075955877, -0.15347749992201365, 0.26838730219647566, 0.1078746647296489, -0.4146283643125561, 0, -0.5524194651733886, 0.9180780656049775]

def positivRandom():
    return random.uniform(0,1)

def negativRandom():
    return random.uniform(-1,0)

def fullRandom():
    return random.uniform(-1,1)
val = -1
for i in range(size):
    indiv = heuristic.clone()
    parameters[3] = val
    val += 0.05

    indiv.set_parameters(parameters)
    indiv.set_functions(functions)
    print(len(parameters), len(functions))
    indiv.save_as_json(f"GeneticAgents/{save}/gen1.json",0)
"""
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
    # isolated tower 4
    parameters.append(positivRandom())
    # isolated tower 3
    parameters.append(positivRandom())
    # isolated tower 2
    parameters.append(positivRandom())
    # isolated tower 1
    parameters.append(positivRandom())
    # enemy isolated tower 4
    parameters.append(negativRandom())
    # enemy isolated tower 3
    parameters.append(negativRandom())
    # enemy isolated tower 2
    parameters.append(negativRandom())
    # enemy isolated tower 1
    parameters.append(negativRandom())
    # wineable tower
    parameters.append(positivRandom())
    # enemy wineable tower
    parameters.append(0)
    # score
    parameters.append(positivRandom())"""



