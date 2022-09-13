#!/usr/bin/env python3

from avalam import *


class HeurisTiktok(Agent):
    def play(self, percepts, player, step, time_left):
        pass
        
    def get_agent_id(self):
        return "HeurisTiktok Agent"

if __name__ == "__main__":
    agent_main(HeurisTiktok())
