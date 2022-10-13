import random

def greedy_play(board, player, step, time_left):
    """Play a greedy action."""
    actions = list(board.get_actions())
            
    def predict_score(board, action):
        board.play_action(action)
        score = int(board.m[action[2]][action[3]])
        board.undo_action()
        return score

    order = [player*5,player*4,player*3,player*2,-player*2,-player*3,-player*4,-player*5]
    srt = {b: i for i, b in enumerate(order)}
    sorted_actions = sorted(actions, key=lambda a: srt[predict_score(board, a)])
    
    return sorted_actions[random.randint(0, len(sorted_actions)*5//100)]