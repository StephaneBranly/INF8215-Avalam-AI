### Observation functions for GeneticBoardEvaluation


def board_score(board):
    return board.get_score() / 20

def board_tower5(board):
    return board.get_number_of_tower_height(5) / 9

def board_tower4(board):
    return board.get_number_of_tower_height(4) / 10

def board_tower3(board):
    return board.get_number_of_tower_height(3) / 10

def board_tower2(board):
    return board.get_number_of_tower_height(2) / 12

def board_tower1(board):
    return board.get_number_of_tower_height(1) / 24

def board_tower5_negative(board):
     return board.get_number_of_tower_height(-5) / 9

def board_tower4_negative(board):
    return board.get_number_of_tower_height(-4) / 10

def board_tower3_negative(board):
    return board.get_number_of_tower_height(-3) / 10

def board_tower2_negative(board):
    return board.get_number_of_tower_height(-2) / 12

def board_tower1_negative(board):
    return board.get_number_of_tower_height(-1) / 24

def board_isolated_tower5(board):
    return board.get_number_of_isolated_tower_height(5) / 9

def board_isolated_tower4(board):
    return board.get_number_of_isolated_tower_height(4) / 10

def board_isolated_tower3(board):
    return board.get_number_of_isolated_tower_height(3) / 10

def board_isolated_tower2(board):
    return board.get_number_of_isolated_tower_height(2) / 12

def board_isolated_tower1(board):
    return board.get_number_of_isolated_tower_height(1) / 24

def board_isolated_tower5_negative(board):
    return board.get_number_of_isolated_tower_height(-5) / 9

def board_isolated_tower4_negative(board):
    return board.get_number_of_isolated_tower_height(-4) / 10

def board_isolated_tower3_negative(board):
    return board.get_number_of_isolated_tower_height(-3) / 10

def board_isolated_tower2_negative(board):
    return board.get_number_of_isolated_tower_height(-2) / 12

def board_isolated_tower1_negative(board):
    return board.get_number_of_isolated_tower_height(-1) / 24

def board_towers_links_1_1(board):
    return board.get_number_of_addable_towers_link(1, 1, 1) / 36

def board_towers_links_1_2(board):
    return board.get_number_of_addable_towers_link(1, 2, 1) / 30

def board_towers_links_1_3(board):
    return board.get_number_of_addable_towers_link(1, 3, 1) / 24

def board_towers_links_1_4(board):
    return board.get_number_of_addable_towers_link(1, 4, 1) / 18

def board_towers_links_2_2(board):
    return board.get_number_of_addable_towers_link(2, 2, 1) / 12

def board_towers_links_2_3(board):
    return board.get_number_of_addable_towers_link(2, 3, 1) / 6


def board_towers_links_1_1_negative(board):
    return board.get_number_of_addable_towers_link(1, 1, -1) / 36

def board_towers_links_1_2_negative(board):
    return board.get_number_of_addable_towers_link(1, 2, -1) / 30

def board_towers_links_1_3_negative(board):
    return board.get_number_of_addable_towers_link(1, 3, -1) / 24

def board_towers_links_1_4_negative(board):
    return board.get_number_of_addable_towers_link(1, 4, -1) / 18

def board_towers_links_2_2_negative(board):
    return board.get_number_of_addable_towers_link(2, 2, -1) / 12

def board_towers_links_2_3_negative(board):
    return board.get_number_of_addable_towers_link(2, 3, -1) / 6

def board_towers_links_1_1_different(board):
    return board.get_number_of_addable_towers_link(1, 1, 0) / 76

def board_towers_links_1_2_different(board):
    return board.get_number_of_addable_towers_link(1, 2, 0) / 60

def board_towers_links_1_3_different(board):
    return board.get_number_of_addable_towers_link(1, 3, 0) / 48

def board_towers_links_1_4_different(board):
    return board.get_number_of_addable_towers_link(1, 4, 0) / 36

def board_towers_links_2_2_different(board):
    return board.get_number_of_addable_towers_link(2, 2, 0) / 24

def board_towers_links_2_3_different(board):
    return board.get_number_of_addable_towers_link(2, 3, 0) / 12

all_board_evaluation_functions = [
    board_score,
    board_tower5,
    board_tower4,
    board_tower3,
    board_tower2,
    board_tower1,
    board_tower5_negative,
    board_tower4_negative,
    board_tower3_negative,
    board_tower2_negative,
    board_tower1_negative,
    board_isolated_tower5,
    board_isolated_tower4,
    board_isolated_tower3,
    board_isolated_tower2,
    board_isolated_tower1,
    board_isolated_tower5_negative,
    board_isolated_tower4_negative,
    board_isolated_tower3_negative,
    board_isolated_tower2_negative,
    board_isolated_tower1_negative,
    board_towers_links_1_1,
    board_towers_links_1_2,
    board_towers_links_1_3,
    board_towers_links_1_4,
    board_towers_links_2_2,
    board_towers_links_2_3,
    board_towers_links_1_1_negative,
    board_towers_links_1_2_negative,
    board_towers_links_1_3_negative,
    board_towers_links_1_4_negative,
    board_towers_links_2_2_negative,
    board_towers_links_2_3_negative,
    board_towers_links_1_1_different,
    board_towers_links_1_2_different,
    board_towers_links_1_3_different,
    board_towers_links_1_4_different,
    board_towers_links_2_2_different,
    board_towers_links_2_3_different,
    ]

class heuristic():
    def __init__(self):
        self._functions = all_board_evaluation_functions
        self._parameters = [1] * len(self._functions)

    def __call__(self, board, player):
        score = 0
        for k in range(len(self._functions)):
            score += self._parameters[k]*self._functions[k](board) * player
        return score