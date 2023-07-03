import pygame
import sys
import chess
import math
from tkinter import messagebox

from utils import PIECE_IMAGES

from AI import alphabeta_pruning

board = chess.Board()

WIDTH = 650

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Crazy Chess")
WHITE = (238, 238, 211)
GREEN = (118, 150, 86)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(col * width)
        self.y = int(row * width)
        self.colour = WHITE

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN, boardM):
        if boardM[self.row][self.col] != "None":
            image = pygame.image.load(PIECE_IMAGES[boardM[self.row][self.col]])
            scaled_image = pygame.transform.scale(image, (int(image.get_width() / 1.8), int(image.get_height() / 1.8)))
            WIN.blit(scaled_image, (self.x, self.y))


def make_grid(rows, width):
    grid = []
    gap = width // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREEN
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def update_display(win, grid, rows, width):
    boardM = []
    for i in range(8):
        arr = [str(board.piece_at(chess.Square((i*8+j)))) for j in range(8)]
        boardM.insert(0,arr)

    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win,boardM)
    draw_grid(win, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    x,y = int(rows), int(columns)
    pos = "" + ['a','b','c','d','e','f','g','h'][x] + f"{8-y}"
    return pos

def machine_move(boardCopy):
    max = -(math.inf)
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    for move in legal_moves:
        result = alphabeta_pruning(boardCopy.copy(),move,3,-(math.inf),math.inf,False)
        if result > max:
            movement = move
            max = result   
    return movement

def main(WIN, WIDTH):
    movement = ""
    grid = make_grid(8, WIDTH)
    while True:
        #pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.set_caption("Crazy Chess | Your turn")
            if event.type == pygame.MOUSEBUTTONDOWN:
                node = Find_Node(pygame.mouse.get_pos(), WIDTH)
                if movement == "":
                    piece = board.piece_at(chess.Square(chess.parse_square(node)))
                    if piece != None and str(piece).isupper(): 
                        movement = node
                    else:
                        print("Not Valid")
                elif movement == node:
                    movement = ""
                else:
                    movement += node
                    move = chess.Move.from_uci(movement)
                    if not move in board.legal_moves:
                        print("Not valid move")
                        movement = ""
                    else:
                        if board.is_capture(move):
                            print('CAPTURA')

                        board.push(chess.Move.from_uci(movement))
                        movement = ""
                        
                        update_display(WIN, grid, 8, WIDTH)

                        #IA
                        pygame.display.set_caption("Crazy Chess | IA turn")
                        movement = machine_move(board.copy())
                        board.push(chess.Move.from_uci(movement))
                        movement = ""

            update_display(WIN, grid, 8, WIDTH)



main(WIN, WIDTH)
