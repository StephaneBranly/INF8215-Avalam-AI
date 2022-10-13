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
    return sorted_actions[random.randint(0, len(sorted_actions)*1//100)]

def random_play(board, player, step, time_left):
    """Play a random action."""
    actions = list(board.get_actions())
    return actions[random.randint(0, len(actions)-1)]

def one_action_heuristic(board, player, step, time_left):
    """Play a random action."""
    actions = list(board.get_actions())

    best_score, best_action = -math.inf, None

    def evaluate(board, action):
        flat_board = np.array(board.m).flatten()
        score = 0
        for i in flat_board:
            if i > 1:
                score += i * player
        return score

    for a in actions:
        board.play_action(a)
        score = evaluate(board, a)
        board.undo_action()
        if score > best_score:
            best_score, best_action = score, a
    return best_action