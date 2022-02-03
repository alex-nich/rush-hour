import Board as b
from copy import deepcopy
from math import ceil
from random import seed
from random import randint
from collections import defaultdict

class Path:
    def __init__(self):
        self.path = []

    def append(self,boards):
        '''appends a list of board objects to path list'''
        for b in boards:
            self.path.append(b)

    def random(self,board, no_of_walks):

        #append original board to path
        self.append([board])

        #return the universe of possible moves given board state
        res = board.next()

        #set seed
        seed(830)

        if not board.done():
            for i in range(no_of_walks):
                #only run again if solution is not found
                if res:
                    #generate random # between 0 and (# of all possible moves - 1)
                    value = randint(0, len(res)-1)
                    #append choosen board to path
                    self.append([res[value]])
                    #regenerate universe of possible moves
                    res = res[value].next()
        
        #print path and total random walks
        self.print_path()
        print("Total random walks (excluding original board): " + str(no_of_walks))
    
    def bfs(self,board):
        ''' find goal state using bfs algorithm '''

        #if board is done, no need to run bfs
        if board.done():
            self.path.append(board)
            self.print_path()
            return print("Total paths explored: 0")

        #variables
        queue = [board]                #-- enqueue first board as first board to explore
        visited = [board.board]        #-- mark first board as visited 
        total_paths = 0                #-- initialize counter
        
        while queue:

            explore = queue.pop(0)          #-- explore first board in queue 
            total_paths = total_paths + 1   #-- increment counter
            res = explore.next()            #-- find universe of possible boards

            #print path that's being explored
            current = explore
            self.path = []
            while current.parent:
                self.path.append(current)
                current = current.parent
                
            if explore.parent:
                print("Path explored: --------------\n")
                self.print_path()

            if res: 
                for b in res:
                    #check if child board = goal state
                    if b.done():
                        goal_state = b
                        queue.clear()   #-- empty queue to terminate while loop
                    
                    #add child board to queue and visited
                    elif b.board not in visited:
                        visited.append(b.board)
                        queue.append(b)
            
        #stored solution path (will be in reverse order)
        current = goal_state
        self.path = []
        while current.parent:
            self.path.append(current)
            current = current.parent
        
        #print solution path and total paths explored
        print("Solution path --------------\n")
        self.print_path()
        print("Total paths explored: " + str(total_paths))

    def calculate_heuristic(self,board):
        '''heuristic used: manhattan distance between car "x" and goal'''
        
        goal = board.escape
        #sorting car coordinates so that first coordinate of 'x' is right-most
        car = sorted(board.cars_coordinates['x'], key=lambda x: x[1], reverse = True)[0]

        #note: x and y coordinates are backwards in entire program :)
        return abs(goal[1] - car[1]) + abs(goal[0] - goal[0])

    def find_lowest_fn(self,open_lst):
        '''returns the board with the lowest f(n)'''
        
        #initializes index and f(n) using first board in open_lst
        to_return=0
        min_fn = open_lst[to_return].g + open_lst[to_return].heuristic                                

        # calculate f(n) for each board in open_lst
        for i, board in enumerate(open_lst):
            fn = board.g + board.heuristic

            #store index of board with lowest f(n)
            if fn <= min_fn: 
                min_fn = fn
                to_return = i
        
        return open_lst[to_return]

    def astar(self,board):
        ''' find goal state using A* algorithm ''' 

        #variables 
        board.g = 0                                       #-- initalize distance from start to current node
        board.heuristic = self.calculate_heuristic(board) #-- set distance from current node to goal
        open_lst = [board]                                #-- add original board to explore list
        closed_lst = []                                   #-- initalize closed list
        total_paths = 0                                   #-- initialize counter

        while open_lst:

            #remove and explore the board with the lowest f(n)
            explore = self.find_lowest_fn(open_lst)
            open_lst.remove(explore)
            total_paths = total_paths + 1

            #print path that's being explored
            current = explore
            self.path = []
            while current.parent:
                self.path.append(current)
                current = current.parent

            if explore.parent:
                print("Path explored: --------------\n")
                self.print_path()

            #check if explore board = goal state
            if explore.done():  
                open_lst.clear()  #-- empty queue to terminate while loop

                #stored solution path (will be in reverse order)
                current = explore
                self.path = []
                while current.parent:
                    self.path.append(current)
                    current = current.parent
            
            #add explore board to closed_lst
            closed_lst.append(explore.board)

            #find universe of possible boards
            res = explore.next()

            if res:
                for b in res:
                    #for each child board, calc g(n) and h(n) and add to open_lst
                    if b.board not in closed_lst:
                        b.g = explore.g + 1
                        b.heuristic = self.calculate_heuristic(b)
                        open_lst.append(b)

        #print solution path and total paths explored
        print("Solution path --------------\n")
        self.print_path()
        print("Total paths explored: " + str(total_paths))

    def print_path(self):
        '''prints the sequence of boards'''

        #variables 
        escape_row = self.path[0].escape[0] #-- store escape row for printing purposes
        beg=0                               #-- used for array slicing
        boards_per_row=6                    #-- used for array slicing

        #correct order of path
        self.path.reverse()
        
        #no need to print newlines if len(path) -le 6
        if len(self.path) < 6:
            end = len(self.path)
        else:
            end=boards_per_row

        for i in range(0,ceil(len(self.path)/boards_per_row)):

            #prints "header"
            for b in self.path[beg:end]:
                print(" ", end ='')
                print("-"*len(self.path[0].board[0]), end = '')
                print(" ", end = " ")
            print("")

            #prints cars of board
            for row_no,j in enumerate(range(len(self.path[0].board))):  
                for i in range(beg,end):
                    print("|", end='')
                    row = self.path[i].board[j]
                    for column in row:
                        print(column, end ='')
                    if row_no == escape_row:
                        print('  ', end = '')    
                    else:
                        print("| ", end = '')
                print('')

            #prints "footer"
            for b in self.path[beg:end]:
                print(" ", end ='')
                print("-"*len(self.path[0].board[0]), end = '')
                print(" ", end = " ")
            print("")

            if len(self.path) > 6:
                #shifting board range
                beg = beg + boards_per_row

                if end + boards_per_row > len(self.path):
                    end = len(self.path)
                else:
                    end = end + boards_per_row
        