# Avalam-AI

Some ideas available [here](https://md.picasoft.net/s/4HP7m5HFT)

## Class diagram

```mermaid
classDiagram
class Heuristic {
  +evaluate(board,player,action) 
  +interprete_params() 
}
click Heuristic href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Heuristic.md" "Detail of the class Heuristic"
Heuristic <|-- Genetic_heuristic
class Genetic_heuristic {
  +evaluate() 
  +interprete_params() 
  +get_default_agent() 
  +set_parameters(parameters) 
  +get_parameters() 
  +mutate(mutation_rate) 
  +crossover(other) 
  +save_as_json(filename,score) 
  +load_from_json(filename,index) 
}
click Genetic_heuristic href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Genetic_heuristic.md" "Detail of the class Genetic_heuristic"
Genetic_heuristic <|-- Genetic_1_action_heuristic
Genetic_heuristic <|-- Genetic_single_loop_heuristic
class Genetic_single_loop_heuristic {
  +evaluate(board,player) 
  +get_default_agent() 
}
click Genetic_single_loop_heuristic href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Genetic_single_loop_heuristic.md" "Detail of the class Genetic_single_loop_heuristic"
class Genetic_1_action_heuristic {
  +evaluate(board,player,action) 
  +get_default_agent() 
}
click Genetic_1_action_heuristic href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Genetic_1_action_heuristic.md" "Detail of the class Genetic_1_action_heuristic"
Genetic_1_action_heuristic <|-- Genetic_mult_actions_heuristic
class Genetic_mult_actions_heuristic {
  +evaluate(init_board,current_board,player,action) 
  +get_default_agent() 
}
click Genetic_mult_actions_heuristic href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Genetic_mult_actions_heuristic.md" "Detail of the class Genetic_mult_actions_heuristic"
class Agent {
  +hasEvolved() 
  +initialize(percepts,players,time_left) 
  +play(percepts,player,step,time_left) 
}
click Agent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Agent.md" "Detail of the class Agent"
Agent <|-- EvolvedAgent
class EvolvedAgent {
  +hasEvolved() 
  +finished(steps,winner,reason,player,game_id,pool_id) 
  +pool_ended(pool_results,player,pool_id) 
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +get_agent_id() 
}
click EvolvedAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/EvolvedAgent.md" "Detail of the class EvolvedAgent"
EvolvedAgent <|-- GreedyAgent
EvolvedAgent <|-- RandomAgent
EvolvedAgent <|-- GeneticAgent
EvolvedAgent <|-- MonteCarloAgent
EvolvedAgent <|-- StepAnalystPlayer
EvolvedAgent <|-- Viewer
class Viewer {
  +init_viewer(board,game) 
  +playing(step,player) 
  +update(step,action,player) 
  +replay(trace,speed) 
}
click Viewer href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Viewer.md" "Detail of the class Viewer"
Viewer <|-- ConsoleViewer
class ConsoleViewer {
  +init_viewer(board,game) 
  +playing(step,player) 
  +update(step,action,player) 
  +play(percepts,player,step,time_left) 
  +finished(steps,winner,reason) 
}
click ConsoleViewer href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/ConsoleViewer.md" "Detail of the class ConsoleViewer"
class StepAnalystPlayer {
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +pool_ended(pool_results,player,pool_id) 
  +get_agent_id() 
}
click StepAnalystPlayer href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/StepAnalystPlayer.md" "Detail of the class StepAnalystPlayer"
class MonteCarloAgent {
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +pool_ended(pool_results,player,pool_id) 
  +get_agent_id() 
}
click MonteCarloAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/MonteCarloAgent.md" "Detail of the class MonteCarloAgent"
class MonteCarlo {
  +mcts(board,player,step,iterations,time_limit,tree) 
  +node_dict(player,parent,action_made) 
  +select(state,board) 
  +expand(n_leaf,board) 
  +simulate(board,player,current_player) 
  +backpropagate(v,n_child,board) 
  +best_action(state) 
  +uct_score(node) 
  +save_tree(tree) 
  +load_tree() 
  +go_down_tree(tree,initial_board,current_board) 
  +tree_to_mermaid(state) 
  +tree_to_mermaid_rec(state) 
  +state_to_string(state) 
}
click MonteCarlo href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/MonteCarlo.md" "Detail of the class MonteCarlo"
MonteCarlo <|-- MonteCarloAgent
class GeneticAgent {
  +setup(agent,parser,args) 
  +load_best_individu(gen) 
  +load_agents_of_pool() 
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +play_agent(agent,percepts,player,step,time_left) 
  +finished(steps,winner,reason,player,game_id,pool_id) 
  +load_agent(individu,generation) 
  +default_agent() 
  +save_stats() 
  +pool_ended(pool_results,player,pool_id) 
  +get_agent_id() 
  +generate_stats_file() 
}
click GeneticAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/GeneticAgent.md" "Detail of the class GeneticAgent"
GeneticAgent <|-- ObservationNN1actionAgent
GeneticAgent <|-- Heuristic1ActionAgent
GeneticAgent <|-- Heuristic2ActionAgent
class Heuristic2ActionAgent {
  +get_agent_id() 
  +play_agent(agent,percepts,player,step,time_left) 
  +default_agent() 
  +generate_stats_file() 
}
click Heuristic2ActionAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Heuristic2ActionAgent.md" "Detail of the class Heuristic2ActionAgent"
class Heuristic1ActionAgent {
  +play_agent(agent,percepts,player,step,time_left) 
  +default_agent() 
  +generate_stats_file() 
}
click Heuristic1ActionAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/Heuristic1ActionAgent.md" "Detail of the class Heuristic1ActionAgent"
class ObservationNN1actionAgent {
  +play_agent(agent,percepts,player,step,time_left) 
  +default_agent() 
}
click ObservationNN1actionAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/ObservationNN1actionAgent.md" "Detail of the class ObservationNN1actionAgent"
class RandomAgent {
  +hasEvolded() 
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +get_agent_id() 
}
click RandomAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/RandomAgent.md" "Detail of the class RandomAgent"
class GreedyAgent {
  +play(percepts,player,step,time_left,game_id,pool_id) 
  +get_agent_id() 
}
click GreedyAgent href "https://github.com/StephaneBranly/Avalam-AI/blob/main/doc/GreedyAgent.md" "Detail of the class GreedyAgent"
```