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

### Observation functions for GeneticBoardEvaluation


def single_loop_tower5(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 5:
        return 1
    else:
        return 0

def single_loop_tower4(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 4:
        return 1
    else:
        return 0

def single_loop_tower3(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 3:
        return 1
    else:
        return 0

def single_loop_tower2(board,player,i,j,isolated = None):
    if board.m[i][j]*player == 2:
        return 1
    else:
        return 0

def enemy_single_loop_tower5(board,player,i,j,isolated = None):
    return single_loop_tower5(board,-player,i,j)

def enemy_single_loop_tower4(board,player,i,j,isolated = None):
    return single_loop_tower4(board,-player,i,j)

def enemy_single_loop_tower3(board,player,i,j,isolated = None):
    return single_loop_tower3(board,-player,i,j)

def enemy_single_loop_tower2(board,player,i,j,isolated = None):
    return single_loop_tower2(board,-player,i,j)

def single_loop_isolated_tower(board,player,i,j,isolated = None):
    if isolated is None:
        isolated = not board.is_tower_movable(i,j)
    if isolated:
        return 1
    else:
        return 0

def enemy_single_loop_isolated_tower(board,player,i,j,isolated = None):
    return single_loop_isolated_tower(board,-player,i,j,isolated)

def single_loop_isolated_tower_heigt(board,player,i,j,height,isolated = None):
    if isolated is None:
        isolated = not board.is_tower_movable(i,j)
    if board.m[i][j]*player == height and isolated:
        return 1
    else:
        return 0

def single_loop_isolated_tower5(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,5,isolated)

def single_loop_isolated_tower4(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,4,isolated)

def single_loop_isolated_tower3(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,3,isolated)

def single_loop_isolated_tower2(board,player,i,j,isolated = None):
    return single_loop_isolated_tower_heigt(board,player,i,j,2,isolated)

def enemy_single_loop_isolated_tower5(board,player,i,j,isolated = None):
    return single_loop_isolated_tower5(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower4(board,player,i,j,isolated = None):
    return single_loop_isolated_tower4(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower3(board,player,i,j,isolated = None):
    return single_loop_isolated_tower3(board,-player,i,j,isolated)

def enemy_single_loop_isolated_tower2(board,player,i,j,isolated = None):
    return single_loop_isolated_tower2(board,-player,i,j,isolated)

# note : check if wineable by creating a tower of 5 not by isolating
def wineable_tower(board,player,i,j,isolated = None):
    total = 0
    if(abs(board.m[i][j]) == 5 or abs(board.m[i][j]) == 0):
        return 0
    for k in range(i-1,i+2):
        for l in range(j-1,j+2):
            if k>=0 and k<9 and l>=0 and l<9:
                if abs(board.m[i][j])+abs(board.m[k][l]) == 5 and (board.m[k][l]*player > 0 or board.m[i][j]*player > 0):
                    total += 1
    return total

def enemy_wineable_tower(board,player,i,j,isolated = None):
    return wineable_tower(board,-player,i,j)

def score(board,player):
    return board.get_score()*player


def remaining_actions(board,player):
    return sum(1 for _ in board.get_actions())

all_board_evaluation_functions = [
single_loop_isolated_tower,enemy_single_loop_isolated_tower,single_loop_tower5,single_loop_tower4,single_loop_tower3,single_loop_tower2,enemy_single_loop_tower5,enemy_single_loop_tower4,enemy_single_loop_tower3,enemy_single_loop_tower2,single_loop_isolated_tower5,single_loop_isolated_tower4,single_loop_isolated_tower3,single_loop_isolated_tower2,enemy_single_loop_isolated_tower5,enemy_single_loop_isolated_tower4,enemy_single_loop_isolated_tower3,enemy_single_loop_isolated_tower2,wineable_tower,enemy_wineable_tower,score,remaining_actions
    ]

all_whole_board_functions = [score, remaining_actions]

class heuristic():
    def __init__(self):
        # adresses des fonctions heuristiques utilisees
        self._functions = all_board_evaluation_functions

        # poids associes aux fonctions heuristiques, poids appris par apprentissage genetique
        self._parameters = [0.7531176053979906, -0.9075462161427894, 0.8952718536462769, -0.6879246438336827, 1, -0.5996165085179597, -1, 0.6598047558023344, 0.2348649286205129, -0.6517161165953501, 0.6766789003215798, 0.9108230478252497, 0.9253009293924904, 0.6441422626481039, -0.6796899746975041, -0.9264074543289749, -0.10767028050408345, -0.20542447964201394, 0.026258067278687736, -0.9445264261844135, 0.6792933962912484, 0.0979788374941244]

    def __call__(self, board, player):
        score = 0
        start_index_whole_board = len(self._functions)

        for (i,j) in board.get_real_board():
            isolated = not board.is_tower_movable(i,j)
            for k in range(len(self._functions)):
                # les fonctions qui concerne l'entiereté du plateau (et non juste une tour) se trouvent a la fin de la liste, si on en rencontre une, break 
                if self._functions[k] in all_whole_board_functions:
                    start_index_whole_board = k
                    break

                score += self._parameters[k]*self._functions[k](board,player,i,j,isolated)

        # certaines fonctions heuristiques sont appliquees sur l'ensemble du plateau
        for k in range(start_index_whole_board,len(self._functions)):
            score += self._parameters[k]*self._functions[k](board,player)
        return score