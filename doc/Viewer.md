# Viewer
Back to [readme menu](../README.md)

Interface for an Avalam viewer and human agent.
## Attributes
### ```init_viewer(board,game)```
Initialize the viewer.
 #### Arguments:
* ```board ```: initial board
 

----

### ```playing(step,player)```
Player player is currently playing step step.

----

### ```update(step,action,player)```
Update the viewer after an action has been played.
 #### Arguments:
* ```step ```: current step number
* ```action ```: action played
* ```player ```: player that has played
 

----

### ```replay(trace,speed)```
Replay a game given its saved trace.

----

