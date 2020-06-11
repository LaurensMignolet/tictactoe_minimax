#!/usr/bin/python

import copy
from pprint import pprint
import random

class Node():
    def __init__(self, board):
        self.board = board
        self.parent = None
        self.value = 0
        self.children = []
    
    def add_child(self, node):
        self.children.append(Child(node))


class Child():
    def __init__(self, node):
        self.node = node

def assign_value(board):
    #x wins value = 1, o wins value = -1, draw = 0
    
    #check horizontal
    for i in range(len(board)):
        if(board[i][0] == "X" and board[i][1] == "X" and board[i][2] == "X"):
            return 1
        if(board[i][0] == "O" and board[i][1] == "O" and board[i][2] == "O"):
            return -1
    
    #check vertical
    for i in range(len(board[0])):
        if(board[0][i] == "O" and board[1][i] == "O" and board[2][i] == "O"):
            return -1
    
        if(board[0][i] == "X" and board[1][i] == "X" and board[2][i] == "X"):
            return 1
    
        
    #check diagonal
    if((board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X") or (board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X")):
        return 1
    if((board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O") or (board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O")):
        return -1
    return 0

def get_plays(board, is_x_turn):
    char = "O"
    if(is_x_turn):
        char = "X"
    
    boards = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            b = copy.deepcopy(board)
            if(board[i][j] == ""):
                b[i][j] += char
                boards.append(b)

    if(len(boards) == 0):
        return "full"
    
    return boards

def generate_tree(start_board, counter):
    g = False
    if(counter%2 == 0):
        g = True
    boards = get_plays(start_board.board, g)
    counter += 1

    if boards != "full":
        for board in boards:
            node = Node(board)
            node.parent = start_board
            node.value = assign_value(board)
            start_board.add_child(node)
            
            if(node.value != 1 and node.value != -1):
                generate_tree(node, counter)
            
           
                if(g == True):
                    min = 5
                    for child in node.children:
                        if child.node.value < min:
                            min = child.node.value
                    node.value = min
                else:
                    max = -5
                    for child in node.children:
                        if child.node.value > max:
                            max = child.node.value
                    node.value = max

def print_grid(grid):
    print("x     0   1   2")
    for i in range(len(grid)):
        print("y " + str(i) + " " + str(grid[i]))

def play(tree):
    #the ai wants to minimize the score
    #you want to maximize the score

    print("\nspecify the x and y coordinates where you want to place an X")
    x = int(input("x: "))
    y = int(input("y: ")) 

    next_b = None

    for i in range(len(tree.children)):
        if(tree.children[i].node.board[y][x] == 'X'):
            next_b = tree.children[i].node
    print_grid(next_b.board)
    
    if(assign_value(next_b.board) == 1):
        print("concratzzzz! u won!")
    else:

        #ai will 0now search child node with least value
        print("\nAI is playing ...")
        min = next_b.children[0].node

        for i in range(1, len(next_b.children)):
            if next_b.children[i].node.value < min.value:
                min = next_b.children[i].node

        print_grid(min.board)

        if(assign_value(min.board) == -1):
            print("The AI Won. \n\nStep 1: win tic tac toe... \nStep 2: TAKE OVER THE WORLD!")
        else:
            play(min)


#eerste zet is random        
bord = [
["", "" , ""],
["", "", ""],
["", "", ""]
]
x = random.randint(0,2)
y = random.randint(0,2)
bord[x][y] += "O"

start_node = Node(bord)
start_node.parent = None

generate_tree(start_node,0)


print_grid(start_node.board)
play(start_node)


