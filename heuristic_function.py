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
        self._parameters = [1, 0.23925245828455366, -0.8181484992958412, 0.28686914814889386, -0.7216321371209762, 0.15360213462978645, -1, -1, -0.6765322286790754, -1, -1, 1, 0.03582411297467614, 0.5577908243743128, 1, -0.5121882152638122, -1, -0.9435076009143804, -1, -0.6735918128472957, 0.33117466761938186, -1, -0.4836084740661424, 0.24786234817358, -0.39480510777050437, 0.4036063877761802, -0.5674668997876433, -1, -0.41343415388698634, 0.8954955111776148, -0.000610865097223634, 0.05884335158860998, -0.05153401225549792, 1, 0.46976303813562237, 0.5217812967782662, 1, -0.7307078732950549, -0.5063841152387378]

    def __call__(self, board, player):
        score = 0
        for k in range(len(self._functions)):
            score += self._parameters[k]*self._functions[k](board) * player
        return score