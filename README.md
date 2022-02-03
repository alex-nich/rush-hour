# rush-hour
Rush Hour is a sliding block puzzle where the goal is to get the goal car to the exit by moving the surrounding cars in a strictly linear fashion. Ultimately, this children game is a computational search problem and therefore can be solved using traditional search algorithms such as Breadth First Search and A*.

Assumptions made: none

Potential issues: Sometimes when calling bfs(), when next() is called, it invokes a maxrecursion error due to the deepcopy() method. 
				  I'm not sure why, but it only happens at random and very seldomly.

To run:
* give +rwx permissions to Board.py, Path.py, and rushhour.py
* bash run.sh *command* *[board]*
* list of possible commands:
  - *print*: prints the starting board
  - *done*: returns True is the starting board is in a solved state and False otherwise
  - *next*: prints all the possible next moves given a starting board
  - *random*: takes 10 random walks given all possible states after a single move
  - *bfs*: solves the given starting board using Breadth First Search
  - *astar*: solves the given starting board using A*
