# GeneticAgent
Back to [readme menu](../readme.md)

## Attributes
### setup(agent,parser,args)
### load_best_individu(gen)
### load_agents_of_pool()
### play(percepts,player,step,time_left,game_id,pool_id)
### play_agent(agent,percepts,player,step,time_left)

        here define the action of your agent
        
### finished(steps,winner,reason,player,game_id,pool_id)
### load_agent(individu,generation)
### default_agent()
returns the agent's core (NN, Genetic Heuristic, ...)
### save_stats()
### pool_ended(pool_results,player,pool_id)
### get_agent_id()
Return an identifier for this agent.
### generate_stats_file()
