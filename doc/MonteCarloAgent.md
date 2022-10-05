# MonteCarloAgent
Back to [readme menu](../README.md)

## Attributes
### play(percepts,player,step,time_left,game_id,pool_id)
### tree_to_mermaid(state)
Return a mermaid graph of the tree.
### tree_to_mermaid_rec(state)
Return a mermaid graph of the tree.
### state_to_string(state)
Return a string representing the state.
### mcts(board,player,iterations)
### node_dict(parent,action_made)
Return a dictionary representing a node in the tree.
### select(state,board)
Select the best node to expand. The board is updated to the state of the node.
### expand(n_leaf,board)
Expand the leaf node n_leaf. The board is updated to the state of the child node.
### simulate(board,player)
Simulate a game from the current state of the board. Return the score of the player. The board is updated to the state of the end of the game.
### backpropagate(v,n_child,board)
Backpropagate the value v to the root of the tree.
### best_action(state)
Return the best action to play from the current state.
### uct_score(node)
Return the UCT score of the node.
### get_agent_id()
