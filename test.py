#!/usr/bin/env python3

from avalam import *
import json
from heuristic.GeneticBoardEvaluation import GeneticBoardEvaluation


def load_best_individu(gen,h):
    try:
        with open(f"GeneticAgents/links/gen{gen}.json") as fp:
            listObj = json.load(fp)
        scores = [cell['score'] for cell in listObj['gen']]
        individu = scores.index(max(scores))
        h.load_from_json(f"GeneticAgents/links/gen{gen}.json", individu)
    except BaseException as e:
        print(f"BaseException raised: {e}")
        print('No more generation')

# main function
if __name__ == "__main__":

    h = GeneticBoardEvaluation()


    for i in range(50):
        load_best_individu(i+352,h)
        h.save_as_json(f"GeneticAgents/links/gen{999}.json", 0)
