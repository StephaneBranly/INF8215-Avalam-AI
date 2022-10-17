# Board
Back to [readme menu](../README.md)

Representation of an Avalam Board.

    self.m is a self.rows by self.columns bi-dimensional array representing the
    board.  The absolute value of a cell is the height of the tower.  The sign
    is the color of the top-most counter (negative for red, positive for
    yellow).

    
## Attributes
### ```max_height```
int([x]) -> integer
int(x, base=10) -> integer
Convert a number or string to an integer, or return 0 if no arguments
are given. If x is a number, return x.__int__(). For floating point
numbers, this truncates towards zero.
If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base. The literal can be preceded by '+' or '-' and be surrounded
by whitespace. The base defaults to 10. Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4

----

### ```initial_board```
Built-in mutable sequence.
If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.

----

### ```clone()```
Return a clone of this object.

----

### ```get_percepts(invert)```
Return the percepts corresponding to the current state.
 If invert is True, the sign of all values is inverted to get the view
of the other player.
 

----

### ```get_towers()```
Yield all towers.
 Yield the towers as triplets (i, j, h):
* ```i ```: row number of the tower
* ```j ```: column number of the tower
* ```h ```: height of the tower (absolute value) and owner (sign)
 

----

### ```is_action_valid(action)```
Return whether action is a valid action.

----

### ```get_tower_actions(i,j)```
Yield all actions with moving tower (i,j)

----

### ```is_tower_movable(i,j)```
Return wether tower (i,j) is movable

----

### ```get_actions()```
Yield all valid actions on this board.

----

### ```play_action(action)```
Play an action if it is valid.
 An action is a 4-uple containing the row and column of the tower to
move and the row and column of the tower to gobble. If the action is
invalid, raise an InvalidAction exception. Return self.
 

----

### ```is_finished()```
Return whether no more moves can be made (i.e., game finished).

----

### ```get_score()```
Return a score for this board.
 The score is the difference between the number of towers of each
player. In case of ties, it is the difference between the maximal
height towers of each player. If self.is_finished() returns True,
this score represents the winner (<0: red, >0: yellow, 0: draw).
 

----

