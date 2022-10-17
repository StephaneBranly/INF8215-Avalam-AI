# MonteCarlo
Back to [readme menu](../README.md)

## Attributes
### ```use_strategy(board,player,step,time_to_play,stats,other_params)```

----

### ```mcts(board,player,step,iterations,time_limit,tree)```
Run the MCTS algorithm.

----

### ```node_dict(player,parent,action_made)```
Return a dictionary representing a node in the tree.

----

### ```select(state,board)```
Select the best node to expand. The board is updated to the state of the node.

----

### ```expand(n_leaf,board)```
Expand the leaf node n_leaf. The board is updated to the state of the child node.

----

### ```simulate(board,player,current_player)```
Simulate a game from the current state of the board. Return the score of the player. The board is updated to the state of the end of the game.

----

### ```backpropagate(v,n_child,board)```
Backpropagate the value v to the root of the tree.

----

### ```best_action(state)```
Return the best action to play from the current state.

----

### ```uct_score(node)```
Return the UCT score of the node.

----

### ```save_tree(tree)```
Save the tree in a file.

----

### ```load_tree()```
Load the tree from a file.

----

### ```go_down_tree(tree,initial_board,current_board)```
Go down the tree by using two different ImprovedBoard

----

### ```tree_to_mermaid(state)```
Return a mermaid graph of the tree.

----

### ```tree_to_mermaid_rec(state)```
Return a mermaid graph of the tree.

----

### ```state_to_string(state)```
Return a string representing the state.

----

