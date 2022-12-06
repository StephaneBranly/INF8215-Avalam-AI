#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, BRANLY Stéphane et GUICHARD Amaury
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
from avalam import *
import time
import math
import random 
from ImprovedBoard import *

class MyAgent(Agent):
    def __init__(self):
        self.c = math.sqrt(2) # constante de UCT
        self.game_time_limit = None
        super().__init__()

    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        start = time.time()

        if time_left:
            # definition du temps de calcul pour la step actuelle
            # temps lineairement decroissant
            if step in [1,2]:
                self.game_time_limit = time_left
            alpha = 0.00001
            beta = 2/18 - 2*alpha
            cstep = (step - step % 2)/2 + 1
            time_to_play = self.game_time_limit * ((beta - alpha)/(1 - 18) * (cstep - 18) + alpha)
            if time_to_play<=1:
                time_to_play = 1
        else:
            time_to_play = 1

        board = dict_to_improved_board(percepts, compute_isolated_towers=False)

        i = 0
        def can_continue():
            if i == 0:
                return True
            if time_to_play:
                return time.time() - start < time_to_play
            raise Exception("No stop condition for MCTS !")

        current_tree =  self.node_dict(player=player)
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

        best_action = self.best_action(current_tree)

        return best_action

    def node_dict(self, player=None, parent=None, action_made=None):
        """Return a dictionary representing a node in the tree."""
        return { "u": 0, "n": 0, "childs": [], "parent": parent, "action_made": action_made, "player": player if player else -parent["player"] }

    def select(self, state, board):
        """Select the best node to expand. The board is updated to the state of the node."""
        if state['action_made']:
            board.play_action(state["action_made"])

        # Si le noeud est une feuille, on le retourne
        if not len(state["childs"]):
            return state

        # Sinon, on selectionne le meilleur noeud fils
        best_score, best_child = -math.inf, None
        for child in state["childs"]:
            if child["n"] == 0:
                return self.select(child, board)

            # Calculate du score UCT du noeud
            score = self.uct_score(child)
            if score > best_score:
                best_score, best_child = score, child
        return self.select(best_child, board)

    def expand(self, n_leaf, board):
        """Expand the leaf node n_leaf. The board is updated to the state of the child node."""
        # Si le noeud est une feuille de l'arbre non simulée, on le retourne
        if n_leaf['n'] == 0:
            return n_leaf
        # Si le noeud est une feuille du jeu, on le retourne
        if board.is_finished():
            return n_leaf

        # Sinon, on étend le noeud 
        actions = list(board.get_actions())
        n_child = None
        for a in actions:
            n_child = self.node_dict(parent=n_leaf, action_made=a)
            n_leaf["childs"].append(n_child)
        if n_child: # On place la board au bon endroit
            board.play_action(n_child['action_made'])
        return n_child


    def simulate(self, board, player, current_player):
        """Simulate a game from the current state of the board. Return the score of the player. The board is updated to the state of the end of the game."""
        while not board.is_finished():
            action = self.simulate_fonction(board, current_player)
            board.play_action(action)
            current_player = -current_player
        
        board_score = board.get_score() * player
        
        # retour du score de la simulation, compris entre 0 et 1
        return 1 if board_score > 0 else 0 if board_score < 0 else 0.5

    def backpropagate(self, v, n_child, board):
        """Backpropagate the value v to the root of the tree."""
        current_node = n_child
        # remontée de l'arbre pour la propagation du score
        while current_node:
            current_node["n"] += 1
            current_node["u"] += v
            current_node = current_node["parent"]

        # remise à zéro de la board
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
            return math.inf
        return node["u"]/node['n'] + self.c * math.sqrt(math.log(node['parent']["n"]) / node["n"])

    def simulate_fonction(self, board, player):
        """Return a random action."""
        return random.choice(list(board.get_actions()))

if __name__ == "__main__":
    agent_main(MyAgent())
