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

    best_score, best_action = -math.inf, None

    def evaluate(board, player, action):
        return board.get_score() * player

    for a in actions:
        board.play_action(a)
        score = evaluate(board, player, a)
        board.undo_action()
        if score > best_score:
            best_score, best_action = score, a
    return best_action

def one_action_heuristic(board, player, step, time_left):
    actions = list(board.get_actions())

    best_score, best_action = -math.inf, None

    def fullObsInit_evaluate(board, player, action):
        score = 0
        # _, _, dx, dy = action
        # real_board = board.get_real_board()
        score += board.get_score() * player * 1
        score += board.get_number_of_tower_height(5 * player) * 0.98
        score += board.get_number_of_tower_height(4 * player) * -0.42
        score += board.get_number_of_tower_height(3 * player) * -0.21
        score += board.get_number_of_tower_height(2 * player) * 0.006
        score += board.get_number_of_tower_height(1 * player) * 0.11
        score += board.get_number_of_tower_height(0 * player) * 0
        score += board.get_number_of_tower_height(-1 * player) * 0.38
        score += board.get_number_of_tower_height(-2 * player) * -0.46
        score += board.get_number_of_tower_height(-3 * player) * -0.60
        score += board.get_number_of_tower_height(-4 * player) * -0.92
        score += board.get_number_of_tower_height(-5 * player) * -1
    
        score += board.get_number_of_isolated_tower_height(5 * player) * -0.82
        score += board.get_number_of_isolated_tower_height(4 * player) * -0.17
        score += board.get_number_of_isolated_tower_height(3 * player) * 0.07
        score += board.get_number_of_isolated_tower_height(2 * player) * 0.06
        score += board.get_number_of_isolated_tower_height(1 * player) * 0.09
        score += board.get_number_of_isolated_tower_height(0 * player) * 0
        score += board.get_number_of_isolated_tower_height(-1 * player) * 0.07
        score += board.get_number_of_isolated_tower_height(-2 * player) * -0.10
        score += board.get_number_of_isolated_tower_height(-3 * player) * -0.26
        score += board.get_number_of_isolated_tower_height(-4 * player) * -0.24
        score += board.get_number_of_isolated_tower_height(-5 * player) * -0.7
        return score

    for a in actions:
        board.play_action(a)
        score = fullObsInit_evaluate(board, player, a)
        board.undo_action()
        if score > best_score:
            best_score, best_action = score, a
    return best_action