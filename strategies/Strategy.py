class Strategy:
    def __init__(self):
        pass

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):
        raise NotImplementedError("use_strategy not implemented")