from avalam import *
import random

b = ImprovedBoard(compute_isolated_towers=True)

def print_data(b):
    print(b)
    sum = 0
    for key in b.addable_towers:
        sum += b.addable_towers[key]
        print(f"{key}\t: {int(b.addable_towers[key])}")
    print(len(list(b.get_actions())))
print_data(b)
actions=list(b.get_actions())
while len(actions) > 18:
    actions = list(b.get_actions())
    b.play_action(random.choice(actions))
    if random.random() < 0.5:
        b.undo_action()
        print("undo")

print_data(b)