from copy import deepcopy
from math import ceil

class Board:
    def __init__(self,board_in):
        self.board = self.setup_board(board_in)
        self.cars_coordinates = self.find_cars_coordinates()
        
        #creating variables for bfs and astar
        self.parent = None
        self.g = None
        self.heuristic = None

    def setup_board(self,board_in):
        '''sets up the board'''

        #variables 
        board_components = board_in.split("|") #-- split the board into rows
        board  = []                            #-- initialize board array

        #generate a 2D array
        for row_no, row in enumerate(board_components):
            for column in row:
                if column == 'x':
                    self.escape = (row_no,len(row)-1)
            board.insert(row_no,list(row))

        return board
    
    def print(self):
        '''prints board state'''

        #prints "header"
        print(" ", end ='')
        print("-"*len(self.board[0]))

        #prints cars of board
        for row_no, row in enumerate(self.board):
            print("|", end='')
            for column in row:
               print(column, end ='')
            if row_no == self.escape[0]:
                print('')    
            else:
                print("|")
            
        #prints "footer"
        print(" ",end='')
        print("-"*len(self.board[0]))    

    def print_boards(self, boards):
        '''prints multiple boards (six per line)'''

        #variables
        beg=0               #-- used for array slicing 
        boards_per_row=6    #-- used for array slicing
        
        #no need to print newlines if len(path) -le 6
        if len(boards) < 6:
            end = len(boards)
        else:
            end=boards_per_row

        for i in range(0,ceil(len(boards)/boards_per_row)):
            
            #prints "header"
            for b in boards[beg:end]:
                print(" ", end ='')
                print("-"*len(boards[0].board[0]), end = '')
                print(" ", end = " ")
            print("")

            #prints cars of board
            for row_no,j in enumerate(range(len(boards[0].board))):  
                for i in range(beg,end):
                    print("|", end='')
                    row = boards[i].board[j]
                    for column in row:
                        print(column, end ='')
                    if row_no == self.escape[0]:
                        print('  ', end = '')    
                    else:
                        print("| ", end = '')
                print('')

            #prints "footer"
            for b in boards[beg:end]:
                print(" ", end ='')
                print("-"*len(boards[0].board[0]), end = '')
                print(" ", end = " ")
            print("")

            if len(boards) > 6:
                #shifting board range
                beg = beg + boards_per_row

                if end + boards_per_row > len(boards):
                    end = len(boards)
                else:
                    end = end + boards_per_row
       
    def done(self):
        '''prints True if the board is in solved state'''
        
        #store the width of the board
        board_width = len(self.board[0])

        #if any part of car "x" is next to right boarder, board is solved
        for row_no, row in enumerate(self.board):
            if row[board_width-1] == "x" and row_no == self.escape[0]:
                return True
        
        return False
        
    def find_cars_coordinates(self):
        '''returns the distinct coordinates for all cars on the board'''
        
        #variables
        cars_coordinates = {} #-- initialize dictionary of cars
        distinct_cars = set() #-- initialize set of distinct cars
        
        for row in self.board:
            for column in row:
                    #only store alphabetic car values
                    if column != " ":
                        distinct_cars.add(column)

  
        for car in distinct_cars:
            #store all coodinates for each car in a list
            list_temp = list()
            for row_no, row in enumerate(self.board):
                for column_no, column in enumerate(row):
                    if column == car:
                        list_temp.append((row_no,column_no))
            #add car and list of coordinates to dictionary
            cars_coordinates[car] = list_temp
                        
        return cars_coordinates

    def clone(self):
        '''returns a deep copy of the board'''     
        return deepcopy(self)

    def get_car_orientation(self, car_coordinates):
        '''returns "h" if car is horizontal, "v" if car is vertical'''

        #determing if car is horizontal (h) or vertal(v)
        #   if all X coordinates are the same, car is horizonal
        #   if all Y coordinates are the same, car is vertical
        if len(set(list(zip(*car_coordinates))[0])) == 1:
            return "h"
        else:
            return 'v'

    def is_left_move_possible(self, car):
        '''return cloned board if car can move left, false is car can't move left'''

        #sort car coodinates so that first coordinate is left-most
        car_coordinates = sorted(self.cars_coordinates[car], key=lambda x: x[1])
        
        #get car orientation
        orientation = self.get_car_orientation(car_coordinates)

        if orientation == "v":
            for coor in car_coordinates:
                #car can't move left if:
                #   - car is at left-most boarder
                #   - car neighbors another car   
                if coor[1] == 0 or self.board[coor[0]][coor[1]-1] != " ":
                    return False
 
        else:
            #if the car is horizontal, check if left-most coordinate neighbors an empty space
            if car_coordinates[0][1] == 0 or self.board[car_coordinates[0][0]][car_coordinates[0][1]-1] != " ":
                return False
        
        return self.move_left(car,car_coordinates,orientation)

    def is_right_move_possible(self, car):
        '''return cloned board if car can move right, false is car can't move right'''

        #sort car coodinates so that first coordinate is right-most
        car_coordinates = sorted(self.cars_coordinates[car], key=lambda x: x[1], reverse = True)
        
        #get board_width
        board_width = len(self.board[0])
        
        #get car orientation
        orientation = self.get_car_orientation(car_coordinates)
  
        if orientation == "v":
            for coor in car_coordinates:
                #car can't move right if:
                #   - car is at right-most boarder
                #   - car neighbors another car   
                if coor[1] == board_width-1 or self.board[coor[0]][coor[1]+1] != " ":
                    return False
 
        else:
            #if the car is horizontal, check if right-most coordinate neighbors an empty space
            if car_coordinates[0][1] == board_width-1 or self.board[car_coordinates[0][0]][car_coordinates[0][1]+1] != " ":
                return False
        
        return self.move_right(car,car_coordinates,orientation)

    def is_up_move_possible(self, car):
        '''return cloned board if car can move up, false is car can't move up'''

        #sort car coodinates so that first coordinate is north-most
        car_coordinates = sorted(self.cars_coordinates[car], key=lambda x: x[0])
        
        #get car orientation
        orientation = self.get_car_orientation(car_coordinates)

        if orientation == "h":
            for coor in car_coordinates:
                #car can't move up if:
                #   - car is at north-most boarder
                #   - car is under another car   
                if coor[0] == 0 or self.board[coor[0]-1][coor[1]] != " ":
                    return False
 
        else:
            #if the car is vertical, check if north-most coordinate is under an empty space
            if car_coordinates[0][0] == 0 or self.board[car_coordinates[0][0]-1][car_coordinates[0][1]] != " ":
                return False
        

        return self.move_up(car, car_coordinates, orientation)

    def is_down_move_possible(self, car):
        '''return cloned board if car can move down, false is car can't move down'''

        #sort car coodinates so that first coordinate is south-most
        car_coordinates = sorted(self.cars_coordinates[car], key=lambda x: x[0], reverse = True)

        #get board_height
        board_height = len(self.board)

        #get car orientation
        orientation = self.get_car_orientation(car_coordinates)
       
        if orientation == "h":
            for coor in car_coordinates:
                #car can't move down if:
                #   - car is at south-most boarder
                #   - car is above another car   
                if coor[0] == board_height-1 or self.board[coor[0]+1][coor[1]] != " ":
                    return False
 
        else:
            #if the car is vertical, check if south-most coordinate is above an empty space
            if car_coordinates[0][0] == board_height-1 or self.board[car_coordinates[0][0]+1][car_coordinates[0][1]] != " ":
                return False
        
        return self.move_down(car,car_coordinates, orientation)

    def move_left(self, car, car_coordinates, orientation):
        '''return cloned board where car is moved to the left'''

        #make a clone
        clone = self.clone()
       
        if orientation == "v":
            for coor in car_coordinates:
                #all car coordinates shift left when car is vertical   
                clone.board[coor[0]][coor[1]-1] = car
                clone.board[coor[0]][coor[1]] = ' '
 
        else:
            #right-most coordinate switches with space (on left of car), when car is horizontal
            clone.board[car_coordinates[-1][0]][car_coordinates[-1][1]] = ' '
            clone.board[car_coordinates[0][0]][car_coordinates[0][1]-1] = car
        
        #update the cloned car coordinates after move is performed
        clone.cars_coordinates = clone.find_cars_coordinates()
        
        return clone

    def move_right(self, car, car_coordinates, orientation):
        '''return cloned board where car is moved to the right'''

        #make a clone
        clone = self.clone()
       
        if orientation == "v":
            for coor in car_coordinates:
                #all car coordinates shift right when car is vertical   
                clone.board[coor[0]][coor[1]+1] = car
                clone.board[coor[0]][coor[1]] = ' '
 
        else:
            #left-most coordinate switches with space (on right of car), when car is horizontal
            clone.board[car_coordinates[-1][0]][car_coordinates[-1][1]] = ' '
            clone.board[car_coordinates[0][0]][car_coordinates[0][1]+1] = car
        
        #update the cloned car coordinates after move is performed
        clone.cars_coordinates = clone.find_cars_coordinates()

        return clone

    def move_up(self, car, car_coordinates, orientation):
        '''return cloned board where car is moved up'''

        #make a clone
        clone = self.clone()
       
        if orientation == "h":
            for coor in car_coordinates:
                #all car coordinates shift up when car is horizontal   
                clone.board[coor[0]][coor[1]] = ' '
                clone.board[coor[0]-1][coor[1]] = car
 
        else:
            #south-most coordinate switches with space (north of car), when car is vertical
            clone.board[car_coordinates[-1][0]][car_coordinates[-1][1]] = ' '
            clone.board[car_coordinates[0][0]-1][car_coordinates[0][1]] = car
        
        #update the cloned car coordinates after move is performed
        clone.cars_coordinates = clone.find_cars_coordinates()

        
        return clone
    
    def move_down(self, car, car_coordinates, orientation):
        '''return cloned board where car is moved down'''

        #make a clone
        clone = self.clone()
       
        if orientation == "h":
            for coor in car_coordinates:
                #all car coordinates shift down when car is horizontal   
                clone.board[coor[0]][coor[1]] = ' '
                clone.board[coor[0]+1][coor[1]] = car
 
        else:
            #north-most coordinate switches with space (south of car), when car is vertical
            clone.board[car_coordinates[-1][0]][car_coordinates[-1][1]] = ' '
            clone.board[car_coordinates[0][0]+1][car_coordinates[0][1]] = car
        
        #update the cloned car coordinates after move is performed
        clone.cars_coordinates = clone.find_cars_coordinates()
        
        return clone
    
    def next_for_car(self, car):
        '''returns a list of boards for all possible of moves given one car'''
        possible_boards = []

        res = self.is_left_move_possible(car)

        #if car can move left once, check if it can be moved left again
        while (res):
            res.parent = self
            possible_boards.append(res)
            res = res.is_left_move_possible(car)

        res = self.is_right_move_possible(car)
        #if car can move right once, check if it can be moved right again
        while (res):
            res.parent = self
            possible_boards.append(res)
            res = res.is_right_move_possible(car)

        res = self.is_up_move_possible(car)
        #if car can move up once, check if it can be moved up again
        while (res):
            res.parent = self
            possible_boards.append(res)
            res = res.is_up_move_possible(car)

        res = self.is_down_move_possible(car)
        #if car can move down once, check if it can be moved down again
        while (res):
            res.parent = self
            possible_boards.append(res)
            res = res.is_down_move_possible(car)

        return possible_boards

    def next(self):
        '''returns a list of boards for all possible of moves given all cars'''
        all_possible_moves = []

        #only run if board is NOT in done state
        if not (self.done()):
           
            #find possible moves for each car
            for car in sorted(self.cars_coordinates.keys()):
                res = self.next_for_car(car)

                if res:
                    for board in res:
                        #append moves to universe
                        all_possible_moves.append(board)
            
            return all_possible_moves #sorted(all_possible_moves)
