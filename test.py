from avalam import *

b = Board()


"""arr1 = [[1,2,3],[4,5,6],[7,8,9]]
tp1 = tuple(map(tuple, arr1))
tp2 = tuple(map(lambda e : tuple(reversed(e)) , arr1))


t1 = tuple(map(tuple, b.m))

t4 = tuple(map(lambda e : tuple(reversed(e)) , reversed(b.m)))


h1 = hash(t1)

h4 = hash(t4)

print(h1)
print(h4)"""

for i in range(0,9):
    for j in range(0,9):
        if b.m[i][j] != 0:
            print('(',i,',',j,')',end=",")



