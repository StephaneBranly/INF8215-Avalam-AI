from avalam import *

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

        self.addable_towers = {
            111: 0,
            121: 0,
            131: 0,
            141: 0,
            221: 0,
            231: 0,
            110: 0,
            120: 0,
            130: 0,
            140: 0,
            220: 0,
            230: 0,     
            -111: 0,
            -121: 0,
            -131: 0,
            -141: 0,
            -221: 0,
            -231: 0,     
        }
       
        self.available_actions = []

        for i in range(self.rows):
            for j in range(self.columns):
                if (i, j) in self.real_board:
                    if self.compute_isolated_towers:
                        actions = list(self.get_tower_actions(i, j))
                        self.available_actions += actions
                        self.actions_by_tower[i][j]=len(actions)
                        if self.actions_by_tower[i][j] == 0:
                            self.number_of_isolated_towers[self.m[i][j]] += 1
                        else:
                            for a in actions:
                                self.compute_addable_towers(a, 1/2)
                    self.number_of_towers[self.m[i][j]] += 1

    def get_mirror_action(self, action):
        return (action[2], action[3], action[0], action[1])
    
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
                        self.compute_addable_towers(a, -1)

                        self.available_actions.remove(a)
                        if a[0] != action[0] or a[1] != action[1]:
                            self.available_actions.remove(self.get_mirror_action(a))
                            if self.actions_by_tower[a[0]][a[1]] == 0:
                                self.number_of_isolated_towers[self.m[a[0]][a[1]]] += 1

                    a = (action[0] + i, action[1] + j, action[0], action[1])
                    if self.is_action_valid(a):
                        self.actions_by_tower[a[0]][a[1]] -= 1
                        self.compute_addable_towers(a, -1)

                        self.available_actions.remove(a)
                        if a[0] != action[2] or a[1] != action[3]:
                            self.available_actions.remove(self.get_mirror_action(a))
                            if self.actions_by_tower[a[0]][a[1]] == 0:
                                self.number_of_isolated_towers[self.m[a[0]][a[1]]] += 1
            self.compute_addable_towers(action, +1)

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
                        self.available_actions.append(a)
                        self.available_actions.append(self.get_mirror_action(a))
                        if self.actions_by_tower[a[0]][a[1]] == 1:
                            self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1
                        self.compute_addable_towers(a, 1)

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
                            self.available_actions.remove(a)
                            self.available_actions.remove(self.get_mirror_action(a))
                            self.compute_addable_towers(a, -1)
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
                            self.compute_addable_towers(a, 1)

                            self.available_actions.append(a)
                            if a[0] != action[0] or a[1] != action[1]:
                                self.available_actions.append(self.get_mirror_action(a))
                                if self.actions_by_tower[a[0]][a[1]] == 1:
                                    self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1

                        a = (action[0] + i, action[1] + j, action[0], action[1])
                        if self.is_action_valid(a):
                            self.actions_by_tower[a[0]][a[1]] += 1
                            self.actions_by_tower[a[2]][a[3]] += 1
                            self.compute_addable_towers(a, 1)

                            self.available_actions.append(a)
                            if a[0] != action[2] or a[1] != action[3]:
                                self.available_actions.append(self.get_mirror_action(a))
                                if self.actions_by_tower[a[0]][a[1]] == 1:
                                    self.number_of_isolated_towers[self.m[a[0]][a[1]]] -= 1
                self.compute_addable_towers(action, -1)
                

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

    def compute_addable_towers(self, action, delta):
        from_tower = self.m[action[0]][action[1]]
        to_tower = self.m[action[2]][action[3]]
        key = None
        if from_tower > 0 and to_tower > 0:
            key = 100 * from_tower + 10 * to_tower + 1 if from_tower < to_tower else 100 * to_tower + 10 * from_tower + 1
        elif from_tower < 0 and to_tower < 0:
            key = 100 * from_tower + 10 * to_tower - 1 if from_tower > to_tower else 100 * to_tower + 10 * from_tower - 1
        else:
            key = abs(100 * from_tower) + abs(10 * to_tower) if abs(from_tower) < abs(to_tower) else abs(100 * to_tower) + abs(10 * from_tower)

        if key:
            self.addable_towers[key] += delta
    
    def get_real_board(self,not_zero=False):
        if not_zero:
            return [x for x in self.real_board if self.m[x[0]][x[1]] != 0]
        return self.real_board

    def get_number_of_tower_height(self, height):
        return self.number_of_towers[height]

    def get_number_of_isolated_tower_height(self, height):
        """
        Returns the number of isolated towers of a given height.

        Arguments:
            height {int} -- Height of the tower
        """
        if self.compute_isolated_towers == False:
            raise Warning("Compute isolated towers is not enabled")
        return self.number_of_isolated_towers[height]

    def get_number_of_addable_towers_link(self, from_height, to_height, player):
        """ 
        Returns the number of addable towers between two towers of a given height.

        Arguments:
            from_height {int} -- Height of the towe
            to_height {int} -- Height of the tower
            player {int} -- Player of the towers (1 or -1 or 0 for two towers from different players)
        """
        if self.compute_isolated_towers == False:
            raise Warning("Compute isolated towers is not enabled")

        key = None
        if from_height < to_height:
            key = 100 * from_height + 10 * to_height + abs(player)
        else:
            key = 100 * to_height + 10 * from_height + abs(player)
        if player:
            key *= player
        return int(self.addable_towers[key])

    def get_tower_actions_len(self, i, j):
        return self.actions_by_tower[i][j]

    def get_score(self):
        score = 0

        for i in range(-5, 6):
            score += self.number_of_towers[i] * (1 if i > 0 else -1 if i < 0 else 0)
        if score == 0:
            return self.number_of_towers[5] - self.number_of_towers[-5]
        return score

    def get_actions(self):
        if self.compute_isolated_towers:
            for a in self.available_actions:
                yield a
        else:
            for a in super().get_actions():
                yield a

def dict_to_improved_board(dictio, compute_isolated_towers=False):
    board = ImprovedBoard(percepts=dictio['m'], compute_isolated_towers=compute_isolated_towers)
    board.m = dictio['m']
    board.rows = dictio['rows']
    board.max_height = dictio['max_height']

    return board