

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