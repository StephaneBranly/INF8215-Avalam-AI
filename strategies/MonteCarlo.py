import math
import json
import gzip
import time
import random

from strategies.Strategy import Strategy

class MonteCarlo(Strategy):
    def __init__(self, c=math.sqrt(2), play_fn=None, node_score_fn=None):
        self.c = c
        self.tree = None
        self.root_board = None
        self.play_fn = play_fn

        if not self.play_fn:
            Warning("No play function provided to MCTS. Using default random play function.")
            self.play_fn = lambda board, player, step, time_limit: random.choice(list(board.get_actions()))

        if not node_score_fn:
            self.node_score_fn = self.uct_score
        super().__init__()

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):
        action, iterations, new_tree, new_board = self.mcts(board, player, step, time_limit=time_to_play)
        if stats:
            print(f"MonteCarlo simulations: {iterations}")
        return action

    def mcts(self, board, player, step, iterations=None, time_limit=None, tree=None):
        """Run the MCTS algorithm."""
        start = time.time()
        i = 0
        def can_continue():
            if i == 0:
                return True
            if iterations:
                return i < iterations
            if time_limit:
                return time.time() - start < time_limit
            raise Exception("No stop condition for MCTS !")

        current_tree = tree if tree else self.node_dict(player=player)
        while can_continue():
            try:
                i += 1
                n_leaf = self.select(current_tree, board)
                n_child = self.expand(n_leaf, board)
                if n_child is None:
                    return self.best_action(current_tree)
                v = self.simulate(board, player, n_child["player"])
                self.backpropagate(v, n_child, board)
            except Exception as e:       
                raise e
        
        # if step == 1:
        #     self.save_tree(tree)
        #     raise Exception("Saved tree")
        new_tree, new_board = None, None
        best_action = self.best_action(current_tree)
        if tree:
            for child in current_tree["childs"]:
                if child['action_made'] == best_action:
                    new_tree = child
                    new_board = board.clone()
                    new_board.play_action(best_action)
                    break
        return best_action, current_tree['n'], new_tree, new_board
    
    def node_dict(self, player=None, parent=None, action_made=None):
        """Return a dictionary representing a node in the tree."""
        return { "u": 0, "n": 0, "childs": [], "parent": parent, "action_made": action_made, "player": player if player else -parent["player"] }

    def select(self, state, board):
        """Select the best node to expand. The board is updated to the state of the node."""
        if state['action_made']:
            board.play_action(state["action_made"])

        # If node is leaf, return it
        if not len(state["childs"]):
            return state

        # Else, select the best child
        best_score, best_child = -math.inf, None
        for child in state["childs"]:
            if child["n"] == 0:
                return self.select(child, board)

            # Calculate the score of the child
            score = self.node_score_fn(child)
            if score > best_score:
                best_score, best_child = score, child
        return self.select(best_child, board)

    def expand(self, n_leaf, board):
        """Expand the leaf node n_leaf. The board is updated to the state of the child node."""
        if board.is_finished():
            return n_leaf
        actions = list(board.get_actions())
        n_child = None
        for a in actions:
            n_child = self.node_dict(parent=n_leaf, action_made=a)
            n_leaf["childs"].append(n_child)
        if n_child:
            board.play_action(n_child['action_made'])
        return n_child

    def simulate(self, board, player, current_player):
        """Simulate a game from the current state of the board. Return the score of the player. The board is updated to the state of the end of the game."""
        while not board.is_finished():
            action = self.play_fn(board, current_player, 0, None)
            board.play_action(action)
            current_player = -current_player
        return board.get_score() * player

    def backpropagate(self, v, n_child, board):
        """Backpropagate the value v to the root of the tree."""
        current_node = n_child
        while current_node:
            current_node["n"] += 1
            current_node["u"] += v
            current_node = current_node["parent"]
        board.undo_all_actions()
        return current_node

    def best_action(self, state):
        """Return the best action to play from the current state."""
        best_score, best_action = -math.inf, None
        for child in state["childs"]:
            score = child['n']
            if score > best_score:
                best_score, best_action = score, child['action_made']
        return best_action

    def uct_score(self, node):
        """Return the UCT score of the node."""
        if node["n"] == 0:
            return -math.inf
        return node["u"] + self.c * math.sqrt(math.log(node['parent']["n"]) / node["n"])

    def save_tree(self, tree):
        """Save the tree in a file."""
        stack = [tree]
        while len(stack):
            current = stack.pop()
            del current["parent"]
            
            if not len(current['childs']):
                del current['childs']
            else:
                for child in current["childs"]:
                    stack.append(child)
        with gzip.open("./strategies/MCTS/tree.json", 'w') as f:
            f.write(json.dumps(tree).encode('utf-8'))                       

    def load_tree(self):
        """Load the tree from a file."""
        try:
            with gzip.open("./strategies/MCTS/tree.json", 'r') as f:
                tree = json.loads(f.read().decode('utf-8'))
            stack = [tree]
            tree['parent'] = None
            while len(stack):
                current = stack.pop()
                if "childs" in current:
                    for child in current["childs"]:
                        child["parent"] = current
                        stack.append(child)
                else:
                    current["childs"] = []
            return tree
        except:
            return self.node_dict()

    def go_down_tree(self, tree, initial_board, current_board):
        """Go down the tree by using two different ImprovedBoard"""
        new_tree = None
        action_made = None
        for child in tree['childs']:
            initial_board.play_action(child['action_made'])
            if initial_board.get_hash() == current_board.get_hash():
                new_tree = child
                action_made = child['action_made']
                break
            initial_board.undo_action()
        return new_tree, action_made
    
    def tree_to_mermaid(self, state):
        """Return a mermaid graph of the tree."""
        mermaid = "graph TD\n"
        mermaid += self.tree_to_mermaid_rec(state)
        return mermaid

    def tree_to_mermaid_rec(self, state):
        """Return a mermaid graph of the tree."""
        mermaid = ""
        id_ = 0
        stack = [(state, 0, id_)]

        while len(stack):
            current = stack.pop()  
            for child in current[0]["childs"]:
                id_ += 1
                child_state = (child, current[1] + 1, id_)
                mermaid += f"{self.state_to_string(current)} -->|{','.join([str(a) for a in child['action_made']])}| {self.state_to_string(child_state)}\n"
                stack.append(child_state)
        return mermaid

    def state_to_string(self, state):
        """Return a string representing the state."""
        return f"id{state[2]}((u = {str(state[0]['u'])} n = {str(state[0]['n'])}))"
