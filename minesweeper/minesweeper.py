import random
import sys
import re

class Board:
    def __init__(self, dimension, num_bombs):
        self.dimension = dimension
        self.num_bombs = num_bombs
        self.dug = set() # return coordinates e.g. {[0,0]}
        self.board = self.make_new_board()
        # create board
   
    
    def __str__(self):
        visible_board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        for row in range(self.dimension):
            for col in range(self.dimension):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '     
        
        string_rep = f'   '
        for r in range(self.dimension):
            string_rep += f"{r} "
        string_rep += f"\n{len(string_rep) * '-'}"
        string_rep += "\n"    
        for r in range(self.dimension):
            string_rep += f"{r}||"
            string_rep += "|".join(visible_board[r])
            string_rep += "|"
            string_rep += '\n'
        return string_rep
    
    
    def make_new_board(self):
        board = []
        for _ in range(self.dimension):
            board.append([None for _ in range(self.dimension)])
        bombs_planted = 0 
        while bombs_planted < self.num_bombs:
            x_coord = random.randint(0, self.dimension - 1)    
            y_coord = random.randint(0, self.dimension - 1)
            if board[x_coord][y_coord] != '*':
                board[x_coord][y_coord] = '*'
                bombs_planted += 1
            else: 
                continue
        return board    


    def assign_values_to_board(self):
        for r in range(self.dimension):
            for c in range(self.dimension):
                if self.board[r][c] == '*':
                    continue
                else:
                    self.board[r][c] = self.get_neighboring_bombs(r, c)


    def get_neighboring_bombs(self, row, col):
        value = 0
        for r in range(max(0,row - 1), min(self.dimension,row + 2)):
            for c in range(max(0,col - 1), min(self.dimension, col + 2)):
                if r == row and c == col:
                    continue 
                if self.board[r][c] == '*':
                    value += 1
        return value


    def dig(self, row, col):
        if (row, col) in self.dug:
            return
        else:
            self.dug.add((row, col))    
            if self.board[row][col] == '*':
                print("Game over!")
                sys.exit()
            if self.get_neighboring_bombs(row, col) == 0:
                self.board[row][col] = 0
                for r in range(max(0, row - 1), min(self.dimension, row + 2)):
                    for c in range(max(0, col - 1), min(self.dimension, col + 2)):
                        if r == row and c == col:
                            continue
                        else:
                            self.dig(r, c)
            else:
                self.board[row][col] = self.get_neighboring_bombs(row, col)
                
                
def play(dim=10, bombs=10):
    board = Board(dim, bombs)
    
    while len(board.dug) < (dim*dim):
        print(board)
        while True:
            try:
                row, col = re.split(",", input('Make a selection(row,col): '))
                row = int(row)
                col = int(col)
                break
            except (ValueError, TypeError, UnboundLocalError):
                print("\nERROR: Please type numbers in 'row,col' format!\n")
            
        if (row, col) not in board.dug:
            while True:
                try:
                    board.dig(row, col)
                    break
                except IndexError:
                    print(f"\n ERROR: Please choose row and column between 0-{board.dimension - 1}!\n")
        else:
            print("\nAlready dug here!\n")    
            
            
play()