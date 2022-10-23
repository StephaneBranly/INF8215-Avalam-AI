def count_neighbour_size(board,player,i,j,size):
    c = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i!=0 or j!=0:
                if not board.is_empty((i,j)):
                    if board.m[i][j] == size * player:
                        c+=1
    return c

def count_neighbour_size_0(board,player,i,j):
    return count_neighbour_size(board,player,i,j,0)

def count_neighbour_size_m1(board,player,i,j):
    return count_neighbour_size(board,-player,i,j,1)

def count_neighbour_size_p1(board,player,i,j):
    return count_neighbour_size(board,player,i,j,1)

def count_neighbour_size_m2(board,player,i,j):
    return count_neighbour_size(board,-player,i,j,2)

def count_neighbour_size_p2(board,player,i,j):
    return count_neighbour_size(board,player,i,j,2)

def count_neighbour_size_m3(board,player,i,j):
    return count_neighbour_size(board,-player,i,j,3)

def count_neighbour_size_p3(board,player,i,j):
    return count_neighbour_size(board,player,i,j,3)

def count_neighbour_size_m4(board,player,i,j):
    return count_neighbour_size(board,-player,i,j,4)

def count_neighbour_size_p4(board,player,i,j):
    return count_neighbour_size(board,player,i,j,4)

def count_neighbour_size_m5(board,player,i,j):
    return count_neighbour_size(board,-player,i,j,5)

def count_neighbour_size_p5(board,player,i,j):
    return count_neighbour_size(board,player,i,j,5)