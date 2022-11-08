# -*- coding: utf-8 -*-
"""
Common definitions for the Avalam players.
Copyright (C) 2010 - Vianney le Clément, UCLouvain
Modified by the teaching team of the course INF8215 - 2022, Polytechnique Montréal

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

PLAYER1 = 1
PLAYER2 = -1

class InvalidAction(Exception):

    """Raised when an invalid action is played."""

    def __init__(self, action=None):
        self.action = action


class Board:

    """Representation of an Avalam Board.

    self.m is a self.rows by self.columns bi-dimensional array representing the
    board.  The absolute value of a cell is the height of the tower.  The sign
    is the color of the top-most counter (negative for red, positive for
    yellow).

    """

    # standard avalam
    max_height = 5
    initial_board = [ [ 0,  0,  1, -1,  0,  0,  0,  0,  0],
                      [ 0,  1, -1,  1, -1,  0,  0,  0,  0],
                      [ 0, -1,  1, -1,  1, -1,  1,  0,  0],
                      [ 0,  1, -1,  1, -1,  1, -1,  1, -1],
                      [ 1, -1,  1, -1,  0, -1,  1, -1,  1],
                      [-1,  1, -1,  1, -1,  1, -1,  1,  0],
                      [ 0,  0,  1, -1,  1, -1,  1, -1,  0],
                      [ 0,  0,  0,  0, -1,  1, -1,  1,  0],
                      [ 0,  0,  0,  0,  0, -1,  1,  0,  0] ]
    

    def __init__(self, percepts=initial_board, max_height=max_height,
                       invert=False):
        """Initialize the board.

        Arguments:
        percepts -- matrix representing the board
        invert -- whether to invert the sign of all values, inverting the
            players
        max_height -- maximum height of a tower

        """
        self.m = percepts
        self.rows = len(self.m)
        self.columns = len(self.m[0])
        self.max_height = max_height
        self.m = self.get_percepts(invert)  # make a copy of the percepts

    def __str__(self):
        def str_cell(i, j):
            x = self.m[i][j]
            if x:
                return "%+2d" % x
            else:
                return " ."
        return "\n".join(" ".join(str_cell(i, j) for j in range(self.columns))
                         for i in range(self.rows))

    def clone(self):
        """Return a clone of this object."""
        return Board(self.m)

    def get_percepts(self, invert=False):
        """Return the percepts corresponding to the current state.

        If invert is True, the sign of all values is inverted to get the view
        of the other player.

        """
        mul = 1
        if invert:
            mul = -1
        return [[mul * self.m[i][j] for j in range(self.columns)]
                for i in range(self.rows)]

    def get_towers(self):
        """Yield all towers.

        Yield the towers as triplets (i, j, h):
        i -- row number of the tower
        j -- column number of the tower
        h -- height of the tower (absolute value) and owner (sign)

        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j]:
                    yield (i, j, self.m[i][j])

    def is_action_valid(self, action):
        """Return whether action is a valid action."""
        try:
            i1, j1, i2, j2 = action
            if i1 < 0 or j1 < 0 or i2 < 0 or j2 < 0 or \
               i1 >= self.rows or j1 >= self.columns or \
               i2 >= self.rows or j2 >= self.columns or \
               (i1 == i2 and j1 == j2) or (abs(i1-i2) > 1) or (abs(j1-j2) > 1):
                return False
            h1 = abs(self.m[i1][j1])
            h2 = abs(self.m[i2][j2])
            if h1 <= 0 or h1 >= self.max_height or h2 <= 0 or \
                    h2 >= self.max_height or h1+h2 > self.max_height:
                return False
            return True
        except (TypeError, ValueError):
            return False

    def get_tower_actions(self, i, j):
        """Yield all actions with moving tower (i,j)"""
        h = abs(self.m[i][j])
        if h > 0 and h < self.max_height:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    action = (i, j, i+di, j+dj)
                    if self.is_action_valid(action):
                        yield action

    def is_tower_movable(self, i, j):
        """Return wether tower (i,j) is movable"""
        for action in self.get_tower_actions(i, j):
            return True
        return False

    def get_actions(self):
        """Yield all valid actions on this board."""
        for i, j, h in self.get_towers():
            for action in self.get_tower_actions(i, j):
                yield action

    def play_action(self, action):
        """Play an action if it is valid.

        An action is a 4-uple containing the row and column of the tower to
        move and the row and column of the tower to gobble. If the action is
        invalid, raise an InvalidAction exception. Return self.

        """
        if not self.is_action_valid(action):
            raise InvalidAction(action)
        i1, j1, i2, j2 = action
        h1 = abs(self.m[i1][j1])
        h2 = abs(self.m[i2][j2])
        if self.m[i1][j1] < 0:
            self.m[i2][j2] = -(h1 + h2)
        else:
            self.m[i2][j2] = h1 + h2
        self.m[i1][j1] = 0
        return self

    def is_finished(self):
        """Return whether no more moves can be made (i.e., game finished)."""
        for action in self.get_actions():
            return False
        return True

    def get_score(self):
        """Return a score for this board.

        The score is the difference between the number of towers of each
        player. In case of ties, it is the difference between the maximal
        height towers of each player. If self.is_finished() returns True,
        this score represents the winner (<0: red, >0: yellow, 0: draw).

        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] < 0:
                    score -= 1
                elif self.m[i][j] > 0:
                    score += 1
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
        return score

class ImprovedBoard(Board):
    mask = [[True , True , False, False, True , True , True , True , True ],
            [True , False, False, False, False, True , True , True , True ],
            [True , False, False, False, False, False, False, True , True ],
            [True , False, False, False, False, False, False, False, False],
            [False, False, False, False, True , False, False, False, False],
            [False, False, False, False, False, False, False, False, True ],
            [True , True , False, False, False, False, False, False, True ],
            [True , True , True , True , False, False, False, False, True ],
            [True , True , True , True , True , False, False, True , True ]]

    def __init__(self, percepts=Board.initial_board, max_height=Board.max_height, invert=False, last_action=None, compute_isolated_towers=False):
        self.last_action = last_action if last_action else []
        self.real_board = [(0 , 2),(0 , 3),(1 , 1),(1 , 2),(1 , 3),(1 , 4),(2 , 1),(2 , 2),(2 , 3),(2 , 4),(2 , 5),(2 , 6),(3 , 1),(3 , 2),(3 , 3),(3 , 4),(3 , 5),(3 , 6),(3 , 7),(3 , 8),(4 , 0),(4 , 1),(4 , 2),(4 , 3),(4 , 5),(4 , 6),(4 , 7),(4 , 8),(5 , 0),(5 , 1),(5 , 2),(5 , 3),(5 , 4),(5 , 5),(5 , 6),(5 , 7),(6 , 2),(6 , 3),(6 , 4),(6 , 5),(6 , 6),(6 , 7),(7 , 4),(7 , 5),(7 , 6),(7 , 7),(8 , 5),(8 , 6)]
        self.actions_by_tower = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        super().__init__(percepts, max_height, invert)
    
        self.number_of_towers = {
            -5: 0,
            -4: 0,
            -3: 0,
            -2: 0,
            -1: 0,
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

        self.compute_isolated_towers = compute_isolated_towers
        self.number_of_isolated_towers = {
            -5: 0,
            -4: 0,
            -3: 0,
            -2: 0,
            -1: 0,
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
       
        for i in range(self.rows):
            for j in range(self.columns):
                if (i, j) in self.real_board:
                    if self.compute_isolated_towers:
                        self.actions_by_tower[i][j]=len([_ for _ in self.get_tower_actions(i, j)])
                        if self.actions_by_tower[i][j] == 0:
                            self.number_of_isolated_towers[self.m[i][j]] += 1
                    self.number_of_towers[self.m[i][j]] += 1


    
    def play_action(self, action):
        if not self.is_action_valid(action):
            print(self)
            print(action)
            print(self.last_action)
        
        # Before Action
        ## Tower count
        self.number_of_towers[self.m[action[0]][action[1]]] -= 1
        self.number_of_towers[self.m[action[2]][action[3]]] -= 1

        ## Available actions count
        if self.compute_isolated_towers:
            for i in range(-1,2):
                for j in range(-1,2):
                    a = (action[2] + i, action[3] + j, action[2], action[3])
                    if self.is_action_valid(a):
                        self.actions_by_tower[a[0]][a[1]] -= 1
                        if self.actions_by_tower[a[0]][a[1]] == 0 and (action[2]+i != action[0] or a[1] != action[1]):
                            self.number_of_isolated_towers[self.m[a[0]][a[1]]] += 1

                    a = (action[0] + i, action[1] + j, action[0], action[1])
                    if self.is_action_valid(a):
                        self.actions_by_tower[a[0]][a[1]] -= 1
                        if self.actions_by_tower[a[0]][a[1]] == 0 and (a[0] != action[2] or a[1] != action[3]):
                            self.number_of_isolated_towers[self.m[a[0]][a[1]]] += 1
        
        ## Save action
        self.last_action.append((action, self.m[action[0]][action[1]], self.m[action[2]][action[3]]))

        # Action
        r = super().play_action(action)

        # After Action
        ## Tower count
        self.number_of_towers[self.m[action[2]][action[3]]] += 1
        
        ## Available actions count
        if self.compute_isolated_towers:
            self.actions_by_tower[action[0]][action[1]] = 0
            self.actions_by_tower[action[2]][action[3]] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    a = (action[2] + i, action[3] + j, action[2], action[3])
                    if self.is_action_valid(a):
                        self.actions_by_tower[a[0]][a[1]] += 1
                        self.actions_by_tower[a[2]][a[3]] += 1
                        if self.actions_by_tower[a[0]][a[1]] == 1:
                            self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1

            if self.actions_by_tower[action[2]][action[3]] == 0:
                self.number_of_isolated_towers[self.m[action[2]][action[3]]] += 1
        
        return r

    def undo_action(self):
        if len(self.last_action):
            action, s, e = self.last_action.pop()

            # Before Undo Action
            ## Tower count
            self.number_of_towers[self.m[action[2]][action[3]]] -= 1

            ## Available actions count
            if self.compute_isolated_towers:
                for i in range(-1,2):
                    for j in range(-1,2):
                        a = (action[2] + i, action[3] + j, action[2], action[3])
                        if self.is_action_valid(a):
                            self.actions_by_tower[a[0]][a[1]] -= 1
                            if self.actions_by_tower[a[0]][a[1]] == 0:
                                self.number_of_isolated_towers[self.m[a[0]][a[1]]] += 1
                if self.actions_by_tower[action[2]][action[3]] == 0:
                    self.number_of_isolated_towers[self.m[action[2]][action[3]]] -= 1

            # Undo Action
            self.m[action[0]][action[1]] = s
            self.m[action[2]][action[3]] = e

            # After Undo Action
            ## Tower count
            self.number_of_towers[s] += 1
            self.number_of_towers[e] += 1

            ## Available actions count
            if self.compute_isolated_towers:
                self.actions_by_tower[action[2]][action[3]] = -1
                self.actions_by_tower[action[0]][action[1]] = -1
            
                for i in range(-1,2):
                    for j in range(-1,2):
                        a = (action[2] + i, action[3] + j, action[2], action[3])
                        if self.is_action_valid(a):
                            self.actions_by_tower[a[0]][a[1]] += 1
                            self.actions_by_tower[a[2]][a[3]] += 1
                            if self.actions_by_tower[a[0]][a[1]] == 1 and (a[0] != action[0] or a[1] != action[1]):
                                self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1

                        a = (action[0] + i, action[1] + j, action[0], action[1])
                        if self.is_action_valid(a):
                            self.actions_by_tower[a[0]][a[1]] += 1
                            self.actions_by_tower[a[2]][a[3]] += 1
                            if self.actions_by_tower[a[0]][a[1]] == 1 and (a[0] != action[2] or a[1] != action[3]):
                                self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1

                

        else:
            raise Exception("No move to undo")

    def undo_all_actions(self):
        while len(self.last_action):
            self.undo_action()

    def clone(self):
        """Return a clone of this object."""
        return ImprovedBoard(self.m, last_action=self.last_action.copy(), compute_isolated_towers=self.compute_isolated_towers)
    
    def get_hash(self):
        """Return a hash of this object."""
        return hash(str(self.m))

    def get_useful_towers(self):
        useful_towers = []
        for (i,j) in self.get_real_board():
                useful = False
                if self.m[i][j] != 0:
                    for k in range(i-1, i+2):
                        for l in range(j-1, j+2):
                            if l > 0 and k > 0 and l < 9 and k < 9:
                                if (self.m[k][l] == 0 and (k,l) in self.get_real_board()) or self.m[k][l] not in [0, 1, -1]:
                                    useful = True
                if useful:
                    useful_towers.append((i, j))
        return useful_towers

    def is_wall(self, i, j):
        return not self.mask[i][j]

    
    def get_real_board(self,not_zero=False):
        if not_zero:
            return [x for x in self.real_board if self.m[x[0]][x[1]] != 0]
        return self.real_board

    def get_number_of_tower_height(self, height):
        return self.number_of_towers[height]

    def get_number_of_isolated_tower_height(self, height):
        if self.compute_isolated_towers == False:
            raise Warning("Compute isolated towers is not enabled")
        return self.number_of_isolated_towers[height]

    def get_tower_actions_len(self, i, j):
        return self.actions_by_tower[i][j]

    def get_score(self):
        score = 0

        for i in range(-5, 6):
            score += self.number_of_towers[i] * (1 if i > 0 else -1 if i < 0 else 0)
        if score == 0:
            return self.number_of_towers[5] - self.number_of_towers[-5]
        return score

def dict_to_improved_board(dictio, compute_isolated_towers=False):
    board = ImprovedBoard(percepts=dictio['m'], compute_isolated_towers=compute_isolated_towers)
    board.m = dictio['m']
    board.rows = dictio['rows']
    board.max_height = dictio['max_height']

    return board

def dict_to_board(dictio):
    """Return a clone of the board object encoded as a dictionary."""
    clone_board = Board()
    clone_board.m = dictio['m']
    clone_board.rows = dictio['rows']
    clone_board.max_height = dictio['max_height']

    return clone_board

def load_percepts(filename):
    """Load percepts from a CSV file."""
    f = None
    try:
        f = open(filename, "r")
        import csv
        percepts = []
        for row in csv.reader(f):
            if not row:
                continue
            row = [int(c.strip()) for c in row]
            if percepts:
                assert len(row) == len(percepts[0]), \
                       "rows must have the same length"
            percepts.append(row)
        return percepts
    finally:
        if f is not None:
            f.close()


class Agent:

    """Interface for an Arlecchino agent"""
    def hasEvolved(self):
        return False

    def initialize(self, percepts, players, time_left):
        """Begin a new game.
        The computation done here also counts in the time credit.
        Arguments:
        percepts -- the initial board in a form that can be fed to the Board
            constructor.
        players -- sequence of players this agent controls
        time_left -- a float giving the number of seconds left from the time
            credit for this agent (all players taken together). If the game is
            not time-limited, time_left is None.
        """
        pass

    def play(self, percepts, player, step, time_left):
        """Play and return an action.
        Arguments:
        percepts -- the current board in a form that can be fed to the Board
            constructor.
        player -- the player to control in this step
        step -- the current step number, starting from 1
        time_left -- a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        """
        pass

class EvolvedAgent(Agent):
    """Evolved agent. This agent has new functions used by the game engine to notify the agent of the competition state."""
    def hasEvolved(self):
        return True
    
    def finished(self, steps, winner, reason="", player=None, game_id=None, pool_id=None):
        """The game is finished.
        Arguments:
        steps -- the number of steps played
        winner -- the winner (>0: even players, <0: odd players, 0: draw)
        reason -- a specific reason for the victory or "" if standard
        player -- the player this agent controls (None if not applicable)
        game_id -- the id of the game this step belongs to
        pool_id -- the id of the pool this game belongs to
        """
        pass

    def pool_ended(self, pool_results, player, pool_id=None):
        """The pool is finished.

        Arguments:
        pool_results -- the pool_results object
        player -- the player this agent controls
        game_id -- the id of the game this step belongs to
        """
        pass

    def play(self, percepts, player, step, time_left, game_id=None, pool_id=None):
        """Play and return an action.
        Arguments:
        percepts -- the current board in a form that can be fed to the Board
            constructor.
        player -- the player to control in this step
        step -- the current step number, starting from 1
        time_left -- a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        game_id -- the id of the game this step belongs to
        pool_id -- the id of the pool this game belongs to
        """
        pass

    def get_agent_id(self):
        """Return an identifier for this agent."""
        return "Agent"

def serve_agent(agent, address, port):
    """Serve agent on specified bind address and port number."""
    from xmlrpc.server import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((address, port), allow_none=True)
    server.register_instance(agent)
    print("Listening on ", address, ":", port, sep="")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def agent_main(agent, args_cb=None, setup_cb=None):
    """Launch agent server depending on arguments.
    Arguments:
    agent -- an Agent instance
    args_cb -- function taking two arguments: the agent and an
        ArgumentParser. It can add custom options to the parser.
        (None to disable)
    setup_cb -- function taking three arguments: the agent, the
        ArgumentParser and the options dictionary. It can be used to
        configure the agent based on the custom options. (None to
        disable)
    """
    import argparse

    def portarg(string):
        value = int(string)
        if value < 1 or value > 65535:
            raise argparse.ArgumentTypeError("%s is not a valid port number" %
                                             string)
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", dest="address", default="",
                        help="bind to address ADDRESS (default: *)")
    parser.add_argument("-p", "--port", type=portarg, default=8000,
                        help="set port number (default: %(default)s)")
    if args_cb is not None:
        args_cb(agent, parser)
    args = parser.parse_args()
    if setup_cb is not None:
        setup_cb(agent, parser, args)

    serve_agent(agent, args.address, args.port)