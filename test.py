from avalam import *

b = Board()
b2 = Board()

arr1 = [[1,2,3],[4,5,6],[7,8,9]]
tp1 = tuple(map(tuple, arr1))
tp2 = tuple(map(lambda e : tuple(reversed(e)) , arr1))
b.play_action((8,6,7,6))
b2.play_action((0,2,1,2))

t1 = tuple(map(tuple, b.m))
t2 = tuple(map(lambda e : tuple(reversed(e)) , reversed(b2.m)))
t3 = tuple(map(tuple, b2.m))
t4 = tuple(map(lambda e : tuple(reversed(e)) , reversed(b.m)))


h1 = hash(t1)
h2 = hash(t2)
h3 = hash(t3)
h4 = hash(t4)

print(tuple(map(tuple, b.m)))
print(tuple(map(lambda e : tuple(reversed(e)) , b2.m)))
print(tuple(map(tuple, b2.m)))
print(tuple(map(lambda e : tuple(reversed(e)) , b.m)))

print(t1 == t2)
print(t1 == t3)
print(t1 == t4)
c = 0

print(c)

print(h1,h2,h3,h4)