import os
import time
from heuristic.observation_function import *
from heuristic.GeneticSingleLoop import GeneticSingleLoop
from avalam import ImprovedBoard
import random
import json

class StateGenerator:

    def __init__(self):
        self.heuristic = GeneticSingleLoop(functions=[single_loop_isolated_tower,enemy_single_loop_isolated_tower,single_loop_tower5,single_loop_tower4,single_loop_tower3,single_loop_tower2,enemy_single_loop_tower5,enemy_single_loop_tower4,enemy_single_loop_tower3,enemy_single_loop_tower2,single_loop_isolated_tower5,single_loop_isolated_tower4,single_loop_isolated_tower3,single_loop_isolated_tower2,enemy_single_loop_isolated_tower5,enemy_single_loop_isolated_tower4,enemy_single_loop_isolated_tower3,enemy_single_loop_isolated_tower2,wineable_tower,enemy_wineable_tower,score,remaining_actions],parameters=[0.7531176053979906, -0.9075462161427894, 0.8952718536462769, -0.6879246438336827, 1, -0.5996165085179597, -1, 0.6598047558023344, 0.2348649286205129, -0.6517161165953501, 0.6766789003215798, 0.9108230478252497, 0.9253009293924904, 0.6441422626481039, -0.6796899746975041, -0.9264074543289749, -0.10767028050408345, -0.20542447964201394, 0.026258067278687736, -0.9445264261844135, 0.6792933962912484, 0.0979788374941244])

    def get_random_state(self,depth):
        b = ImprovedBoard()
        for i in range(depth):
            if b.is_finished():
                return b
            actions = list(b.get_actions())
            b.play_action(random.choice(actions))
        return b

    def simulate_single(self,b,a,player):
        b.play_action(a)
        s = self.heuristic.evaluate(b,player,a)
        b.undo_action()
        return s

    def simulate_state(self,board,depth):
        player = 1 if depth%2 == 0 else -1
        win = 0
        nbAction = len(list(board.get_actions()))
        number_of_simulation = nbAction*2
        print("Simulating state with "+str(nbAction)+" actions")
        for i in range(number_of_simulation):
            b = board.clone()
            
            start = time.time()
            while not b.is_finished():
                actions = list(b.get_actions())
                actions.sort(key=lambda a: self.simulate_single(b,a,player),reverse=True)

                b.play_action(actions[random.randint(0,(len(actions)//10)+1)])
                player = -player

            print("Simulation "+str(i+1)+"/"+str(number_of_simulation)+" took "+str(time.time()-start)+"s and "+str(b.get_score())+" points")
            win += 1 if b.get_score() > 0 else 0    
        return win/number_of_simulation

    def save_single_state(self,board,win,depth,save):
        with open(save) as fp:
            listObj = json.load(fp)
            data = {}
            data["board"] = board.get_percepts()
            data["win"] = win
            data["depth"] = depth
            listObj["states"].append(data)
        with open(save,"w") as fp:
            json.dump(listObj,fp)

    def init_savefile(self,save):
        isExist = os.path.exists(save)
        if not isExist:
            with open(save,"w") as fp:
                json.dump({"states":[]},fp)


    def generate_states(self,min_depth,max_depth,number_of_state,save):
        total = (max_depth-min_depth)*number_of_state
        current = 0
        states = {}
        self.init_savefile(save)
        
        for i in range(number_of_state):
            for d in range(min_depth,max_depth):
                b = self.get_random_state(d)
                while b.get_hash() in states:
                    b = self.get_random_state(d)
                win = self.simulate_state(b,d)
                self.save_single_state(b,win,d,save)
                current += 1
                print("Progress: "+str(current)+"/"+str(total)+" "+str(current/total*100)+"%")
                states[b.get_hash()] = (b.get_percepts(),win,d)



if __name__ == "__main__":
    s = StateGenerator()
    s.generate_states(5,30,500,"./states/states.json")
