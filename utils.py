def calculate_genetic_diversity(json_file):
    """Calculate the genetic diversity of a population.

    Args:
        json_file (str): Path to the json file.

    Returns:
        float: Genetic diversity of the population.
    """
    import json, numpy as np, pandas as pd
    with open(json_file, "r") as f:
        population = json.load(f)
    parameters = [ind["parameters"] for ind in population["gen"]]
    df = pd.DataFrame(parameters)

    return df.std(), df.std().mean()

# for i in range(0,14):
#     print("generation "+str(i)+" : \n"+str(calculate_genetic_diversity("NN_MT2/gen"+str(i)+".json"))+"\n------------------")

def key_value_or_default(d, key, default):
    if key in d:
        return d[key]
    else:
        return default