import random
import math
import numpy as np

def greedy_play(board, player, step, time_left):
    """Play a greedy action."""
    actions = list(board.get_actions())
            
    def predict_score(board, action):
        board.play_action(action)
        score = int(board.m[action[2]][action[3]])
        board.undo_action()
        return score

    order = [player*5,player*4,player*3,player*2,-player*2,-player*3,-player*4,-player*5]
    srt = {b: i for i, b in enumerate(order)}
    sorted_actions = sorted(actions, key=lambda a: srt[predict_score(board, a)])
    
    return sorted_actions[0]

def random_play(board, player, step, time_left):
    """Play a random action."""
    actions = list(board.get_actions())
    return actions[random.randint(0, len(actions)-1)]

def best_score(board, player, step, time_left):
    actions = list(board.get_actions())

    def evaluate(board, player, action):
        return board.get_score() * player

    sorted_scores = []
    for a in actions:
        board.play_action(a)
        score = evaluate(board, player, a)
        sorted_scores.append((score, a))
        board.undo_action()

    sorted_scores.sort(key=lambda x: x[0], reverse=True)

    return sorted_scores[random.randint(0, int(len(sorted_scores) * 0.1))][1]

def one_action_heuristic(board, player, step, time_left):
    actions = list(board.get_actions())

    def evaluate(board, player, action):
        score = 0

        score += board.get_score() * player * 1
        score += board.get_number_of_tower_height(5 * player) * 1
        score += board.get_number_of_tower_height(4 * player) * -0.7
        score += board.get_number_of_tower_height(3 * player) * 0.6
        score += board.get_number_of_tower_height(2 * player) * -0.81
        score += board.get_number_of_tower_height(1 * player) * 1
        score += board.get_number_of_tower_height(0 * player) * 0
        score += board.get_number_of_tower_height(-5 * player) * -0.73
        score += board.get_number_of_tower_height(-4 * player) * 0.40
        score += board.get_number_of_tower_height(-3 * player) * -0.7
        score += board.get_number_of_tower_height(-2 * player) * 1
        score += board.get_number_of_tower_height(-1 * player) * 0.7
        # score += board.get_score() * player * 0.88
        # score += board.get_number_of_tower_height(5 * player) * -0.62
        # score += board.get_number_of_tower_height(4 * player) * -0.67
        # score += board.get_number_of_tower_height(3 * player) * 0.47
        # score += board.get_number_of_tower_height(2 * player) * -0.81
        # score += board.get_number_of_tower_height(1 * player) * 1
        # score += board.get_number_of_tower_height(0 * player) * 0
        # score += board.get_number_of_tower_height(-5 * player) * 0.73
        # score += board.get_number_of_tower_height(-4 * player) * -0.40
        # score += board.get_number_of_tower_height(-3 * player) * 1
        # score += board.get_number_of_tower_height(-2 * player) * 1
        # score += board.get_number_of_tower_height(-1 * player) * 0.7
    
        return score

    sorted_scores = []
    for a in actions:
        board.play_action(a)
        score = evaluate(board, player, a)
        sorted_scores.append((score, a))
        board.undo_action()

    sorted_scores.sort(key=lambda x: x[0], reverse=True)

    return sorted_scores[random.randint(0, int(len(sorted_scores) * 0.1))][1]


    
def one_action_heuristic_iso(board, player, step, time_left):
    actions = list(board.get_actions())

    def evaluate(board, player, action):
        params = [0.42071394720114674, 1, -1, 1, -1, 1, 0.5838536982992937, -1, -0.5954259580684425, 0.3312304375677593, 0.44191235823226904, 0.9899212066129495, 0.1799603945101671, 0.918889129472998, 0.10048777312002755, 0.10706584523671503, -0.31524518575522076, -0.9803229565820908, -0.5622079427119793, -1, 0.3012717505458522]
        score = 0

        score += board.get_score() * player * params[0]
        score += board.get_number_of_tower_height(5 * player) * params[1]
        score += board.get_number_of_tower_height(4 * player) * params[2]
        score += board.get_number_of_tower_height(3 * player) * params[3]
        score += board.get_number_of_tower_height(2 * player) * params[4]
        score += board.get_number_of_tower_height(1 * player) * params[5]
        score += board.get_number_of_tower_height(-5 * player) * params[6]
        score += board.get_number_of_tower_height(-4 * player) * params[7]
        score += board.get_number_of_tower_height(-3 * player) * params[8]
        score += board.get_number_of_tower_height(-2 * player) * params[9]
        score += board.get_number_of_tower_height(-1 * player) * params[10]
    
        score += board.get_number_of_isolated_tower_height(5 * player) * params[11]
        score += board.get_number_of_isolated_tower_height(4 * player) * params[12]
        score += board.get_number_of_isolated_tower_height(3 * player) * params[13]
        score += board.get_number_of_isolated_tower_height(2 * player) * params[14]
        score += board.get_number_of_isolated_tower_height(1 * player) * params[15]
        score += board.get_number_of_isolated_tower_height(-5 * player) * params[16]
        score += board.get_number_of_isolated_tower_height(-4 * player) * params[17]
        score += board.get_number_of_isolated_tower_height(-3 * player) * params[18]
        score += board.get_number_of_isolated_tower_height(-2 * player) * params[19]
        score += board.get_number_of_isolated_tower_height(-1 * player) * params[20]
        
        return score

    sorted_scores = []
    for a in actions:
        board.play_action(a)
        score = evaluate(board, player, a)
        sorted_scores.append((score, a))
        board.undo_action()

    sorted_scores.sort(key=lambda x: x[0], reverse=True)

    return sorted_scores[random.randint(0, int(len(sorted_scores) * 0.1))][1]