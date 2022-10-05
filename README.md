# Avalam-AI

Some ideas available [here](https://md.picasoft.net/s/4HP7m5HFT)

## Class diagram

```mermaid
classDiagram
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