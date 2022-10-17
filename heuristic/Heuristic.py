class Heuristic:
    def __init__(self):
        pass

    def evaluate(self, board, player, action=None):
        raise NotImplementedError

    def interprete_params(self):
        return None

    def __call__(self,board,player,action):
        return self.evaluate(board,player,action)
