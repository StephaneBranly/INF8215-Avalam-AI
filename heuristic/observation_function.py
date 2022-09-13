

def finish_tower(board,player,action):
    """Return 1:0:-1 if the action finish a tower of the player"""
    board = board.clone()
    board.play_action(action)
    if board.m[action[2]][action[3]] == player*5:
        return 1
    elif board.m[action[2]][action[3]] == -player*5:
        return -1
    else:
        return 0



def isolate_tower(board,player,action):
    after = board.clone()
    after.play_action(action)
    new_isolated_tower = 0
    for i in range(9):
        for j in range(9):
            if board.is_tower_movable(i,j) and not after.is_tower_movable(i,j) and after.m[i][j]*player > 0:
                new_isolated_tower += 1
    return new_isolated_tower

def use_token(board,player,action):
    """Return 1 if the player use a token, -1 otherwise"""
    if board.m[action[0]][action[1]]*player > 0:
        return 1
    else:
        return -1

def cover_token(board,player,action):
    """Return 1 if the player cover a token, -1 otherwise"""
    if board.m[action[2]][action[3]]*player > 0:
        return 1
    else:
        return -1