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

def one_action_simple_h(board, player, step, time_left):
    actions = list(board.get_actions())

    best_score, best_action = -math.inf, None

    def evaluate(board, player, action):
        flat_board = np.array(board.m).flatten()
        score = 0
        factors = [-.93,.66,.23,-.62,0,0,0,-.6,1,-.69,.9]
        for i in flat_board:
            score += factors[i+5]
        
        return score

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
        score += board.get_number_of_tower_height(5 * player) * 0.84
        score += board.get_number_of_tower_height(4 * player) * 0.05
        score += board.get_number_of_tower_height(3 * player) * -0.74
        score += board.get_number_of_tower_height(2 * player) * -0.17
        score += board.get_number_of_tower_height(1 * player) * 0.8
        score += board.get_number_of_tower_height(0 * player) * 0
        score += board.get_number_of_tower_height(-1 * player) * 0.04
        score += board.get_number_of_tower_height(-2 * player) * 0.03
        score += board.get_number_of_tower_height(-3 * player) * 0.09
        score += board.get_number_of_tower_height(-4 * player) * -0.59
        score += board.get_number_of_tower_height(-5 * player) * -0.99
        score += board.get_score() * player * 0.77
        # for x in range(-1, 1):
        #     for y in range(-1, 1):
        #         i = dx + x
        #         j = dy + y
        #         if (i, j) in real_board:
        #             isolated_tower = not board.is_tower_movable(i,j)
        #             tower_height = board.m[i][j]
        #             # single_loop_isolated_tower
        #             score += (1 if isolated_tower else 0) * 0.96 

        #             # single_loop_tower5
        #             score += (1 if tower_height * player == 5 else 0) * 0.9

        #             # single_loop_tower4
        #             score += (1 if tower_height * player == 4 else 0) * -0.69
            
        #             # single_loop_tower3
        #             score += (1 if tower_height * player == 3 else 0) * 1

        #             # single_loop_tower2
        #             score += (1 if tower_height * player == 2 else 0) * -0.6

        #             # enemy_single_loop_tower5
        #             score += (1 if tower_height * player == -5 else 0) * -0.93

        #             # enemy_single_loop_tower4
        #             score += (1 if tower_height * player == -4 else 0) * 0.66

        #             # enemy_single_loop_tower3
        #             score += (1 if tower_height * player == -3 else 0) * 0.23

        #             # enemy_single_loop_tower2
        #             score += (1 if tower_height * player == -2 else 0) * -0.62

        #             # single_loop_isolated_tower_5
        #             score += (1 if tower_height * player == 5 and isolated_tower else 0) * 0.68 * 2

        #             # single_loop_isolated_tower_4
        #             score += (1 if tower_height * player == 4 and isolated_tower else 0) * 0.91 * 2

        #             # single_loop_isolated_tower_3
        #             score += (1 if tower_height * player == 3 and isolated_tower else 0) * 1 * 2

        #             # single_loop_isolated_tower_2
        #             score += (1 if tower_height * player == 2 and isolated_tower else 0) * 0.64 * 2

        #             # enemy_single_loop_isolated_tower_5
        #             score += (1 if tower_height * player == -5 and isolated_tower else 0) * -0.68 * 2

        #             # enemy_single_loop_isolated_tower_4
        #             score += (1 if tower_height * player == -4 and isolated_tower else 0) * -0.93 * 2

        #             # enemy_single_loop_isolated_tower_3
        #             score += (1 if tower_height * player == -3 and isolated_tower else 0) * -0.73 * 2

        #             # enemy_single_loop_isolated_tower_2
        #             score += (1 if tower_height * player == -2 and isolated_tower else 0) * -0.22 * 2

        #             # enemy_winable_tower
        #             score += (1 if tower_height * player < 0 and not isolated_tower else 0) * -0.93 * 2

        return score

    for a in actions:
        board.play_action(a)
        score = fullObsInit_evaluate(board, player, a)
        board.undo_action()
        if score > best_score:
            best_score, best_action = score, a
    return best_action