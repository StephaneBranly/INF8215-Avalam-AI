# EvolvedAgent
Back to [readme menu](../README.md)

Evolved agent. This agent has new functions used by the game engine to notify the agent of the competition state.
## Attributes
### ```hasEvolved()```

----

### ```finished(steps,winner,reason,player,game_id,pool_id)```
The game is finished.
#### Arguments:
* ```steps ```: the number of steps played
* ```winner ```: the winner (>0: even players, <0: odd players, 0: draw)
* ```reason ```: a specific reason for the victory or "" if standard
* ```player ```: the player this agent controls (None if not applicable)
* ```game_id ```: the id of the game this step belongs to
* ```pool_id ```: the id of the pool this game belongs to


----

### ```pool_ended(pool_results,player,pool_id)```
The pool is finished.
 #### Arguments:
* ```pool_results ```: the pool_results object
* ```player ```: the player this agent controls
* ```game_id ```: the id of the game this step belongs to


----

### ```play(percepts,player,step,time_left,game_id,pool_id)```
Play and return an action.
#### Arguments:
* ```percepts ```: the current board in a form that can be fed to the Board
constructor.
* ```player ```: the player to control in this step
* ```step ```: the current step number, starting from 1
* ```time_left ```: a float giving the number of seconds left from the time
credit. If the game is not time-limited, time_left is None.
* ```game_id ```: the id of the game this step belongs to
* ```pool_id ```: the id of the pool this game belongs to


----

### ```get_agent_id()```
Return an identifier for this agent.

----

