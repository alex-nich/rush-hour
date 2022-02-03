#!/usr/bin/python3
import Board as b
import Path as p
import os.path
import sys

def print_board(*args):

    #use default board is one isn't passed in
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
    
    #create board using arg passed in
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    #call function
    b1.print()

def done(*args):
    
    #use default board is one isn't passed in
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
    
    #create board using arg passed in
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    #call function
    print(str(b1.done()))

def next(*args):
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
   
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    res = b1.next()
    if res:
        b1.print_boards(res)

def random(*args):

    #use default board is one isn't passed in
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
   
    #create board using arg passed in
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    #call function
    p1 = p.Path()
    no_of_random_walks=10
    p1.random(b1,no_of_random_walks)

def bfs(*args):
    #use default board is one isn't passed in
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
   
    #create board using arg passed in
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    #call function
    p1 = p.Path()
    p1.bfs(b1)

def astar(*args):
    if len(args) == 0:
        b1 = b.Board("  o aa|  o   |xxo   |ppp  q|     q|     q")
   
    elif len(args) == 1:
        b1 = b.Board(args[0])
    
    p1 = p.Path()
    p1.astar(b1)

#b.Board(" ooo  |ppp q |xx  qa|rrr qa|b c dd|b c ee")

commands = {
    'print': print_board,
    'done': done,
    'next': next,
    'random': random,
    'bfs': bfs,
    'astar': astar    
}

if __name__ == '__main__':
    command = os.path.basename(sys.argv[1])
    if command in commands:
        commands[command](*sys.argv[2:])