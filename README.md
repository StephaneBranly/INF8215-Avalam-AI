# Avalam-AI

Some ideas available [here](https://md.picasoft.net/s/4HP7m5HFT)

## Class diagram


```mermaid
classDiagram
    Agent <|-- EvolvedAgent
    EvolvedAgent <|-- GeneticAgent
    EvolvedAgent <|-- GreedyAgent
    EvolvedAgent <|-- RandomAgent
    GeneticAgent <|-- Heuristic1ActionAgent
    Heuristic1ActionAgent o-- Genetic_1_action_heuristique : default_agent
    Heuristic <|-- Genetic_1_action_heuristique
    class Agent{
      +initialize()
      +play()
    }
    class EvolvedAgent{
      +finsihed(*args)
      +pool_ended(*args)
      +play(*args, game_id, pool_id)
      +get_agent_id()
    }
    class GeneticAgent{
      +setup(*args)
      +load_best_individu(*args)
      +load_agents_of_pool()
      +play(*args)
      +play_agent(*args)
      +finished(*args)
      +load_agent(*args)
      +default_agent()
      +save_stats()
      +pool_ended(*args)
      +get_agent_id()
    }
    class Heuristic1ActionAgent {
        +play_agent(*args)
        +default_agent()
        +generate_stats()
    }
    class Genetic_1_action_heuristique{
        +evaluate(*args)
        +interprete_params(*args)
        +set_parameters(params)
        +get_parameters()
        +mutate(rate)
        +crossover(other)
        +save_a_json(fname, score)
        +load_from_json(fname, index)
    }
    class Heuristic{
        +evaluate(*args)
        +interpret_params()
    }
            
```