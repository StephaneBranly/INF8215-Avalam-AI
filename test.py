import gzip
import json
from avalam import ImprovedBoard


dic = {}
counter = 0
def tree_to_dic(node,board,depth):
    global counter
    global dic
    hash = board.get_hash()
    if node['n']>=(30-depth)*10:
        if hash not in dic:
            dic[hash] = (board.clone(),node['u'],node['n'])
            #print(board)
            #print((node['u'],node['n'],node['u']/node['n']))
        else:
            if node['n'] > dic[hash][2]:
                dic[hash] = (board.clone(),node['u'],node['n'])
    counter += 1
    #print(board)
    if 'childs' in node:
        for child in node['childs']:
            board.play_action(child['action_made'])
            tree_to_dic(child,board,depth+1)
            board.undo_action()

with gzip.open("./strategies/MCTS/tree.json", 'r') as f:
    tree = json.loads(f.read().decode('utf-8'))
    tree_to_dic(tree,ImprovedBoard(),0)
    print(counter)
    print(len(dic))
    print(tree['n'])
    with open("./strategies/MCTS/dic.json", 'w') as f2:
        f2.write(json.dumps(dic))



