

def finish_tower(boards,player,action):
    """Return 1:0:-1 if the action finish a tower of the player"""
    if boards[0].m[action[0]][action[1]]*player > 0:
        owner = player
    else:
        owner = -player
    if abs(boards[0].m[action[2]][action[3]]) + abs(boards[0].m[action[0]][action[1]]) == 5:
        if owner == player:
            return 1
        else:
            return -1
    else:
        return 0

def isolate_tower(boards,player,action):
    after = boards[1]
    new_isolated_tower = 0
    for i in range(9):
        for j in range(9):
            if boards[0].is_tower_movable(i,j) and not after.is_tower_movable(i,j) and after.m[i][j]*player > 0:
                new_isolated_tower += 1
    return new_isolated_tower

def ennemy_isolate_tower(boards,player,action):
    return isolate_tower(boards,-player,action)

def use_token(boards,player,action):
    """Return 1 if the player use a token, -1 otherwise"""
    if boards[0].m[action[0]][action[1]]*player > 0:
        return 1
    else:
        return -1

def cover_token(boards,player,action):
    """Return 1 if the player cover a token, -1 otherwise"""
    if boards[0].m[action[2]][action[3]]*player > 0:
        return 1
    else:
        return -1

def create_tower4(boards,player,action):
    if boards[0].m[action[0]][action[1]]*player > 0:
        owner = player
    else:
        owner = -player
    if abs(boards[0].m[action[2]][action[3]]) + abs(boards[0].m[action[0]][action[1]]) == 4:
        if owner == player:
            return 1
        else:
            return -1
    else:
        return 0

def create_tower3(boards,player,action):
    if boards[0].m[action[0]][action[1]]*player > 0:
        owner = player
    else:
        owner = -player
    if abs(boards[0].m[action[2]][action[3]]) + abs(boards[0].m[action[0]][action[1]]) == 3:
        if owner == player:
            return 1
        else:
            return -1
    else:
        return 0

def create_tower2(boards,player,action):
    if boards[0].m[action[0]][action[1]]*player > 0:
        owner = player
    else:
        owner = -player
    if abs(boards[0].m[action[2]][action[3]]) + abs(boards[0].m[action[0]][action[1]]) == 2:
        if owner == player:
            return 1
        else:
            return -1
    else:
        return 0


def score_after_action(boards,player,action):
    after = boards[1]
    return after.get_score()*player

def remaining_actions(boards,player,action):
    after = boards[1]
    return sum(1 for _ in after.get_actions())

def score(board,player):
    return board.get_score()*player


def remaining_actions(board,player):
    return sum(1 for _ in board.get_actions())



def mult_create_tower5(boards,player,action):
    towers = 0
    for i in range(9):
        for j in range(9):
            if boards[0].m[i][j]*player != 5 and boards[1].m[i][j]*player == 5:
                towers += 1
    return towers

def mult_create_tower4(boards,player,action):
    towers = 0
    for i in range(9):
        for j in range(9):
            if boards[0].m[i][j]*player != 4 and boards[1].m[i][j]*player == 4:
                towers += 1
    return towers

def mult_create_tower3(boards,player,action):
    towers = 0
    for i in range(9):
        for j in range(9):
            if boards[0].m[i][j]*player != 3 and boards[1].m[i][j]*player == 3:
                towers += 1
    return towers

def mult_create_tower2(boards,player,action):
    towers = 0
    for i in range(9):
        for j in range(9):
            if boards[0].m[i][j]*player != 2 and boards[1].m[i][j]*player == 2:
                towers += 1
    return towers

def enemy_mult_create_tower5(boards,player,action):
    return mult_create_tower5(boards,-player,action)

def enemy_mult_create_tower4(boards,player,action):
    return mult_create_tower4(boards,-player,action)

def enemy_mult_create_tower3(boards,player,action):
    return mult_create_tower3(boards,-player,action)

def enemy_mult_create_tower2(boards,player,action):
    return mult_create_tower2(boards,-player,action)

def single_loop_tower5(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 5:
        return 1
    else:
        return 0

def single_loop_tower4(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 4:
        return 1
    else:
        return 0

def single_loop_tower3(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 3:
        return 1
    else:
        return 0

def single_loop_tower2(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 2:
        return 1
    else:
        return 0

def enemy_single_loop_tower5(board,player,i,j,isolated = None):
    return single_loop_tower5(board,-player,i,j)

def enemy_single_loop_tower4(board,player,i,j,isolated = None):
    return single_loop_tower4(board,-player,i,j)

def enemy_single_loop_tower3(board,player,i,j,isolated = None):
    return single_loop_tower3(board,-player,i,j)

def enemy_single_loop_tower2(board,player,i,j,isolated = None):
    return single_loop_tower2(board,-player,i,j)

def single_loop_isolated_tower(board,player,i,j,isolated = None):
    if isolated is None:
        isolated = not board.is_tower_movable(i,j)
    if isolated:
        return 1
    else:
        return 0

def enemy_single_loop_isolated_tower(board,player,i,j,isolated = None):
    return single_loop_isolated_tower(board,-player,i,j,isolated)

def single_loop_isolated_tower_heigt(board,player,i,j,height,isolated = None):
    if isolated is None:
        isolated = not board.is_tower_movable(i,j)
    if board.m[i][j]*player == height and isolated:
        return 1
    else:
        return 0

def single_loop_isolated_tower5(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,5,isolated)

def single_loop_isolated_tower4(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,4,isolated)

def single_loop_isolated_tower3(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,3,isolated)

def single_loop_isolated_tower2(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,2,isolated)

def enemy_single_loop_isolated_tower5(board,player,i,j,isolated = None):
    return single_loop_isolated_tower5(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower4(board,player,i,j,isolated = None):
    return single_loop_isolated_tower4(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower3(board,player,i,j,isolated = None):
    return single_loop_isolated_tower3(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower2(board,player,i,j,isolated = None):
    return single_loop_isolated_tower2(board,-player,i,j,isolated)

def movable_tower(board,player,i,j,isolated = None):
    if isolated is None:
        isolated = not board.is_tower_movable(i,j)
    if board.m[i][j]*player > 0 and not isolated:
        return 1
    else:
        return 0

def enemy_movable_tower(board,player,i,j,isolated = None):
    return movable_tower(board,-player,i,j,isolated)

# note : check if wineable by creating a tower of 5 not by isolating
def wineable_tower(board,player,i,j,isolated = None):
    total = 0
    if(abs(board.m[i][j]) == 5 or abs(board.m[i][j]) == 0):
        return 0
    for k in range(i-1,i+2):
        for l in range(j-1,j+2):
            if k>=0 and k<9 and l>=0 and l<9:
                if abs(board.m[i][j])+abs(board.m[k][l]) == 5 and (board.m[k][l]*player > 0 or board.m[i][j]*player > 0):
                    total += 1
    return total

def enemy_wineable_tower(board,player,i,j,isolated = None):
    return wineable_tower(board,-player,i,j)





### Observation functions for GeneticBoardEvaluation

def board_score(board, player):
    return board.get_score() * player

def board_tower5(board, player):
    return board.get_number_of_tower_height(5 * player)

def board_tower4(board, player):
    return board.get_number_of_tower_height(4 * player)

def board_tower3(board, player):
    return board.get_number_of_tower_height(3 * player)

def board_tower2(board, player):
    return board.get_number_of_tower_height(2 * player)

def board_tower1(board, player):
    return board.get_number_of_tower_height(1 * player)

def board_tower5_enemy(board, player):
    return board_tower5(board, -player)

def board_tower4_enemy(board, player):
    return board_tower4(board, -player)

def board_tower3_enemy(board, player):
    return board_tower3(board, -player)

def board_tower2_enemy(board, player):
    return board_tower1(board, -player)

def board_tower1_enemy(board, player):
    return board_tower1(board, -player)

