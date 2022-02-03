Name: Alexys Lamkin

Assumptions made: none

Potential issues: Sometimes when calling bfs(), when next() is called, it invokes a maxrecursion error due to the deepcopy() method. 
				  I'm not sure why, but it only happens at random and very seldomly.

To run: (This is personally how I got my code to run TUX, but this could be common sense :))
 - give +rwx permissions to Board.py, Path.py, and rushhour.py
 - execute rush.sh <command> [<board>]
 - this of commands include:
	*print
    *done
    *next
    *random
    *bfs
    *astar
