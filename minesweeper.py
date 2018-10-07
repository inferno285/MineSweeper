#!/bin/python3
import random
import sys
OPEN = '-'
HIDDEN = '#'
MINE = '*'
MAX_SIZE = 100
ADJACENT = [(-1,0), (1, 0), (0, -1), (0, 1), (1, -1), (1, 1), (-1, 1), (-1, -1)]
class Board():

    def __init__(self, width, height, mines=4):
        self.width = width
        self.height = height
        #Underlying board
        self.board = [[OPEN]*width for x in range(height)]
        #A boolean mask to apply for displaying the board
        self.shown = [[False]*width for x in range(height)]
        self.mines = min(mines, width*height-1)
        self.is_over = False
        #Make a list of all possible positions for mines
        possible_positions = list(range(width*height))
        random.shuffle(possible_positions)
        for i in range(self.mines):
            p = possible_positions.pop()
            x = p%width
            y = p//width
            print([x, y, width, height])
            self.add_mine(x, y)
    def is_shown(self,x, y):
        return self.shown[y][x]

    def at_pos(self,x, y):
        return self.board[y][x]
    def increment(self,x, y):
        if self.board[y][x] != OPEN and not check_for_number(self.board[y][x]): return
        if self.board[y][x] == OPEN: self.board[y][x] = 0
        self.board[y][x] += 1

    def add_mine(self,x, y):
        for _x, _y in ADJACENT:
            if x+_x < 0 or x+_x >= self.width: continue
            if y+_y < 0 or y+_y >= self.height: continue
            self.increment(_x+x, _y+y)
        self.board[y][x] = MINE
    def color(self,c):
        c = str(c)
        return c
    def display_board(self, all=False):
        width_len = len(str(self.width))
        height_len = len(str(self.height))
        gap = ' '*width_len
        print('\n'*50)
        print(' '*(height_len+2)+' '.join([str(x+1).rjust(width_len, ' ') for x in range(self.width)]),end='\n\n')
        for i, (row_mask, row) in enumerate(zip(self.shown,self.board)):
            if all:
                print(str(i+1).rjust(height_len+width_len-1, ' ')+'  '+gap.join([str(a) for a in row]))
            else:
                print(str(i+1).rjust(height_len+width_len-1, ' ')+'  '+gap.join([HIDDEN if not a else self.color(b) for a,b in zip(row_mask, row)]))
    def show(self, x, y):
        self.shown[y][x] = True

    def clear(self,x,y):
        self.show(x, y)
        q = [(x, y)]
        while q:
            x, y = q.pop()
            for _x, _y in ADJACENT:
                if x+_x < 0 or x+_x >= self.width: continue
                if y+_y < 0 or y+_y >= self.height: continue
                #if its a number display it
                if check_for_number(self.board[_y+y][_x+x]): 
                    self.show(_x+x, _y+y)
                    continue
                #if its not a number or not an open the continue
                if self.board[_y+y][_x+x] != OPEN: continue
                #if its already shown continue
                if self.is_shown(_x+x,_y+y): continue
                self.show(_x+x,_y+y)
                #Iteratively clear all adjacents
                q.append((_x+x,_y+y))

    def apply_click(self,x, y):
        at_pos = self.at_pos(x, y)
        if self.is_shown(x, y):
            raise Exception(f"Should only be able to click {HIDDEN}'s")
        if at_pos == OPEN:
            self.clear(x, y)
        elif check_for_number(at_pos):
            self.show(x, y)
        else:
            self.show(x, y)
            self.lose()
        if self.check_win():
            self.display_board(True)
            print("Congratulations You Won!")
            self.is_over = True

    def check_win(self):
        revealed = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.is_shown(x, y): revealed += 1
        if revealed + self.mines >= self.width*self.height:
            return True
        return False

    def lose(self):
        self.display_board(True)
        print("OH NO. You hit a mine. Game Over.")
        self.is_over = True

def check_for_number(c):
    if isinstance(c, int):
        return True
    if isinstance(c, str) and c.isdigit():
        return True
    return False
def get_click_pos(board):
    while True:
        print("Enter your next move row first example(4 1):", end='')
        
        try:
            y,x = input().split()
        except KeyboardInterrupt:
            sys.exit()
        except:
            print('Try again Example:4 4')
            continue
        if not x.isdigit():
            print('Row must be a number. Example: 4 4')
            continue
        if not y.isdigit():
            print('Column must be a number. Example: 4 4')
            continue
        y = int(y)
        x = int(x)
        if not 0 < x <= board.width:
            print(f'Column must be a number 1 through {board.width}')
            continue
        if not 0 < y <= board.height:
            print(f'Row must be a number 1 through {board.height}')
            continue
        if board.is_shown(x-1, y-1):
            print(f'You already revealed here. Click a {HIDDEN} to continue.')
            continue
        break
    return (x-1, y-1)

def get_board_input():
    print("Enter your board size.")
    while True:
        print("Width:",end='')
        width = input()
        if not width.isdigit():
            print("Please enter a number")
            continue
        width = int(width)
        if width < 3 or width > MAX_SIZE:
            print(f"Please enter a width between 3 and {MAX_SIZE}")
            continue
        break
    while True:
        print("Height:",end='')
        height = input()
        if not height.isdigit():
            print("Please enter a number")
            continue
        height = int(height)
        if height < 3 or height > MAX_SIZE:
            print(f"Please enter a height between 3 and {MAX_SIZE}")
            continue
        break
    print("Enter how many mines.")
    while True:
        print("Mines:",end='')
        mines = input()
        if not mines.isdigit():
            print("Please enter a number")
            continue
        mines = int(mines)
        if mines < 1 or mines > MAX_SIZE:
            max_mines = height*width-1
            print(f"Please enter a number between 1 and {max_mines}")
            continue
        break
    return (width, height, mines)

#Main loop



print("\nWelcome to minesweeper\n")

board_inputs = get_board_input()

board = Board(*board_inputs)

while not board.is_over:
    board.display_board()
    
    click_x, click_y = get_click_pos(board)

    
    
    board.apply_click(click_x, click_y)


