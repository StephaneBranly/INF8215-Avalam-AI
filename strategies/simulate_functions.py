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

    best_score, best_actions = -math.inf, [None]
    for a in actions:
        board.play_action(a)
        score = evaluate(board, player, a)
        if score > best_score:
            best_score, best_actions = score, [a]
        elif score == best_score:
            best_actions.append(a)
        board.undo_action()

    return random.choice(best_actions)

def one_action_heuristic(board, player, step, time_left):
    actions = list(board.get_actions())

    def fullObsInit_evaluate(board, player, action):
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

    best_score, best_actions = -math.inf, [None]
    for a in actions:
        board.play_action(a)
        score = fullObsInit_evaluate(board, player, a)
        if score > best_score:
            best_score, best_actions = score, [a]
        elif score == best_score:
            best_actions.append(a)
        board.undo_action()

    return random.choice(best_actions)

    # return scores[random.randint(0, int(len(scores) * 0.1))][1]

def one_action_heuristic_iso(board, player, step, time_left):
    actions = list(board.get_actions())

    def fullObsInit_evaluate(board, player, action):
        score = 0

        score += board.get_score() * player * 0.84
        score += board.get_number_of_tower_height(5 * player) * -0.11
        score += board.get_number_of_tower_height(4 * player) * -0.02
        score += board.get_number_of_tower_height(3 * player) * 0.86
        score += board.get_number_of_tower_height(2 * player) * 0.53
        score += board.get_number_of_tower_height(1 * player) * -0.23
        score += board.get_number_of_tower_height(0 * player) * 0
        score += board.get_number_of_tower_height(-5 * player) * -0.07
        score += board.get_number_of_tower_height(-4 * player) * -0.96
        score += board.get_number_of_tower_height(-3 * player) * -0.45
        score += board.get_number_of_tower_height(-2 * player) * -0.86
        score += board.get_number_of_tower_height(-1 * player) * -0.27
    
        score += board.get_number_of_isolated_tower_height(5 * player) * 0.61
        score += board.get_number_of_isolated_tower_height(4 * player) * 0.34
        score += board.get_number_of_isolated_tower_height(3 * player) * 1
        score += board.get_number_of_isolated_tower_height(2 * player) * 1
        score += board.get_number_of_isolated_tower_height(1 * player) * 1
        score += board.get_number_of_isolated_tower_height(0 * player) * 0
        score += board.get_number_of_isolated_tower_height(-5 * player) * -1
        score += board.get_number_of_isolated_tower_height(-4 * player) * -0.47
        score += board.get_number_of_isolated_tower_height(-3 * player) * 0.97
        score += board.get_number_of_isolated_tower_height(-2 * player) * -0.95
        score += board.get_number_of_isolated_tower_height(-1 * player) * -0.07
        
        return score

    best_score, best_actions = -math.inf, [None]
    for a in actions:
        board.play_action(a)
        score = fullObsInit_evaluate(board, player, a)
        if score > best_score:
            best_score, best_actions = score, [a]
        elif score == best_score:
            best_actions.append(a)
        board.undo_action()

    return random.choice(best_actions)

    # return scores[random.randint(0, int(len(scores) * 0.1))][1]