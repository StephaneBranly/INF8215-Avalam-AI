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
import time
from avalam import *
from heuristic_function import *
from ImprovedBoard import *
import math

class MyAgent(Agent):

    def __init__(self):

        self.heuristic_core = heuristic()
        super().__init__()



    def play(self, percepts, player, step, time_left):
        max = -math.inf
        best_action = None
        board = dict_to_improved_board(percepts,True)
        for a in board.get_actions():
            board.play_action(a)
            value = self.heuristic_core(board, player)
            board.undo_action()
            if value > max:
                max = value
                best_action = a
        return best_action


if __name__ == "__main__":
    agent_main(MyAgent())

