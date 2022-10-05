import math
from avalam import *
import random   
import time

class MonteCarloAgent(EvolvedAgent):
    def __init__(self):
        self.c = math.sqrt(2)
    
    """A monte carlo agent."""
    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None): 
        board = dict_to_improved_board(percepts)
        start_time = time.time()
        action = self.mcts(board, player, 5000)
        print(f"Action: {action} for step {step} | Time: {time.time() - start_time}")
        return action

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
                if child["n"] != 0:
                    id_ += 1
                    child_state = (child, current[1] + 1, id_)

                    mermaid += f"{self.state_to_string(current)} -->|{','.join([str(a) for a in child['action_made']])}| {self.state_to_string(child_state)}\n"
                    stack.append(child_state)
        return mermaid

    def state_to_string(self, state):
        """Return a string representing the state."""
        return f"id{state[2]}((u = {str(state[0]['u'])} n = {str(state[0]['n'])}))"

    def mcts(self, board, player, iterations=300):
        tree = self.node_dict()
        start = time.time()
        while time.time()-start <= 40:
            n_leaf = self.select(tree, board)
            n_child = self.expand(n_leaf, board)
            if n_child is None:
                with open("tree.mermaid", "w") as f:
                    f.write(self.tree_to_mermaid(tree))
                return self.best_action(tree)
            v = self.simulate(board, player)
            self.backpropagate(v, n_child, board)
        return self.best_action(tree)
    
    def node_dict(self, parent=None, action_made=None):
        """Return a dictionary representing a node in the tree."""
        return { "u": 0, "n": 0, "childs": [], "parent": parent, "action_made": action_made }

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
            score = self.uct_score(child)
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
            n_child = self.node_dict(n_leaf, a)
            n_leaf["childs"].append(n_child)
        if n_child:
            board.play_action(n_child['action_made'])
        return n_child

    def simulate(self, board, player):
        """Simulate a game from the current state of the board. Return the score of the player. The board is updated to the state of the end of the game."""
        while not board.is_finished():
            actions = list(board.get_actions())
            board.play_action(random.choice(actions))
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
            score = self.uct_score(child)
            if score > best_score:
                best_score, best_action = score, child['action_made']
        return best_action

    def uct_score(self, node):
        """Return the UCT score of the node."""
        if node["n"] == 0:
            return -math.inf
        return node["u"] + self.c * math.sqrt(math.log(node['parent']["n"]) / node["n"])


    def get_agent_id(self):
        return "Monte Carlo Agent"

if __name__ == "__main__":
    agent_main(MonteCarloAgent())
