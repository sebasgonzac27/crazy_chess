import pygame
import sys
import chess
import math

from AI import machine_move, put_piece
from utils import PIECE_IMAGES



# Inicializamos el tablero de ajedrez.
board = chess.Board()
pygame.font.init()

# Definimos el ancho de la ventana.
WIDTH = 650
PADDING = 80

# Creamos una ventana con el ancho y alto definidos.
WIN = pygame.display.set_mode((WIDTH + PADDING, WIDTH +PADDING))

# Establecemos el título de la ventana del programa.
pygame.display.set_caption("Crazy Chess")

# Establecemos los colores RGB
WHITE = (238, 238, 211)
GREEN = (118, 150, 86)
GREEN2 = (88, 117, 69)
YELLOW = (255, 218, 33)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

font_name = pygame.font.get_default_font()
font_path = 'app/fuentes/BebasNeue-Regular.otf'
font = pygame.font.Font(font_path, 21)
font2 = pygame.font.Font(font_path, 22)

class Node:
    """
    Representación de una celda del tablero de ajedrez.
    """

    def __init__(self, row, col, width):
        """
        Inicializa un nodo.

            row : fila en la que se ubica el nodo.
            col : columna en la que se ubica el nodo.
            width : ancho del nodo.
        """
        self.row = row
        self.col = col
        self.x = int(col * width) + PADDING / 2
        self.y = int(row * width) + PADDING / 2
        self.colour = WHITE
        self.selected = False
        


    def draw(self, window):
        """ 
        Dibuja la celda en la ventana de visualización.

            window : ventana de visualización.
            
        """
        if self.selected:
            pygame.draw.rect(window, YELLOW, (self.x, self.y, (WIDTH / 8), (WIDTH / 8)))
        else: pygame.draw.rect(window, self.colour, (self.x, self.y, (WIDTH / 8),(WIDTH / 8) ))


    def setup(self, window, matrix):
        """
        Establece las fichas de ajedrez en el tablero de juego.

            window: ventana de visualización.
            matrix : matriz que representa el tablero de ajedrez.
        """
        # Si la celda en la posición dada no está vacía, crea la imagen, la escala
        # y la ubica en la posición correspondiente.
        if matrix[self.row][self.col] != "None":
            image = pygame.image.load(PIECE_IMAGES[matrix[self.row][self.col]])
            scaled_image = pygame.transform.scale(image, (int(image.get_width() / 1.8), int(image.get_height() / 1.8)))
            window.blit(scaled_image, (self.x, self.y))

def draw_plane(window):
        """
        Dibuja el plano base.
        """
        pygame.draw.rect(window, GREEN2, (0, 0, WIDTH + PADDING , WIDTH + PADDING ))
        
def draw_letters_numbers(window):
    """
    Dibuja las letras y números del tablero.

    """
    
    list_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    list_numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    x,y = 15,70
    x2,y2 = 76,697
    for i in range(8):
        text = font2.render(list_numbers[i], True, WHITE)
        window.blit(text, (x, y))
        y += 81
    for i in range(8):
        text2 = font.render(list_letters[i], True, WHITE)
        window.blit(text2, (x2, y2))
        x2 = x2 + 81.4

def turn_text(window, TURN):
    """
    Dibuja el texto que indica el turno de juego.
    
    """
    if TURN == 0:
        text = font.render("Turno de las blancas:  JUGADOR", True, YELLOW)
        window.blit(text, (240, 9))
    elif TURN == 1:
        text = font.render("Turno de las negras:  IA", True, YELLOW)
        window.blit(text, (240, 9))

def make_grid(size, width):
    """
    Devuelve una cuadrícula de nodos.

        size : representa el número de filas y columnas del tablero.
        width : indica el ancho total de la cuadrícula.
    """
    grid = []

    # Calculamos el ancho de cada casilla.
    gap = width // size

    # Añadimos cada nodo a la cuadrícula.
    for i in range(size):
        grid.append([])

        for j in range(size):
            node = Node(i, j, gap)

            grid[i].append(node)

            # si i + j es un número impar, se pinta de verde la celda.
            if (i + j) % 2 == 1:
                grid[i][j].colour = GREEN

    return grid



def draw_grid(window, size, width):
    """
    Dibuja las líneas de la cuadrícula en la ventana del juego.

        window : ventana de visualización.
        size : número de filas y columnas de la cuadrícula.
        width : ancho total de la cuadrícula.
    """
    # Calculamos el ancho de cada celda.
    # gap = width // 8

    # Pintamos las líneas de color negro.
    # for i in range(size):
    #     pygame.draw.line(window, BLACK, (0 + PADDING / 2, i * gap + PADDING / 2 ), (width + PADDING / 2, i * gap + PADDING / 2 ))
    #     for j in range(size):
    #         pygame.draw.line(window, BLACK, (j * gap + PADDING / 2 , 0 + PADDING / 2), (j * gap + PADDING / 2 , width + PADDING / 2 ))



def update_display(window, grid, rows, width, turn):
    """
    Actualiza la ventana del tablero de ajedrez.

        window : ventana de visualización.
        grid : cuadrícula que representa el tablero de ajedrez.
        rows : número de filas del tablero.
        width : ancho total de la ventana de juego.
    """
    matrix = []
    draw_plane(window)
    turn_text(window, turn)
    draw_letters_numbers(window)
    # Recorremos el tablero y guardamos cada tipo de pieza en la matriz.
    for i in range(8):
        arr = [str(board.piece_at(chess.Square((i * 8 + j)))) for j in range(8)]
        matrix.insert(0, arr)

    # Recorremos de nuevo la cuadrícula y dibujamos cada nodo.
    for row in grid:
        for spot in row:
            spot.draw(window)
            spot.setup(window, matrix)

    # Dibujamos las líneas de la cuadrícula.
    draw_grid(window, rows, width)

    # Actualizamos la ventana de juego para mostrar los cambios hechos.
    pygame.display.update()



def find_node(pos, width):
    """
    Encuentra la posición del nodo en el tablero de ajedrez a partir de una posición
    dada en píxeles en la ventana del juego.

        pos : tupla que representa la posición en pixeles (x, y) dentro de la ventana.
        width : ancho total de la ventana de juego.
    """
    # Calculamos el ancho de cada nodo.
    interval = width / 8

    # Definimos la fila y columna del nodo.
    y, x = pos

    y = y - PADDING / 2
    x = x - PADDING / 2

    row =  y // interval
    col = x // interval

    x, y = int(row), int(col)

    # Obtenemos la posicíon del nodo en la notación del ajedrez.
    pos = "" + ['a','b','c','d','e','f','g','h'][x] + f"{8 - y}"

    return pos

def main(window, width):
    
    """
    Función principal que ejecuta el juego de ajedrez.

        window : ventana de visualización.
        width : ancho total de la ventana.
    """
    # Creamos una variable para almacenar el movimiento del jugador.
    movement = ""
    turn_text(window, 0)
    captured_piece = None
    prev_x = None
    prev_y = None
    # Creamos la cuadrícula del tablero de ajedrez.
    grid = make_grid(8, width)

    while True:
        for event in pygame.event.get():
            # Si se ejecuta un evento QUIT, se cierra el programa.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Establecemos el título de la ventana de juego.
            pygame.display.set_caption("Crazy Chess | Your turn")

            # Si se presiona el mouse.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtenemos el nodo que ha sido seleccionado.
                node = find_node(pygame.mouse.get_pos(), width)

                click_p = pygame.mouse.get_pos()

                # Calculamos el ancho de cada nodo.
                interval = width / 8
                # Definimos la fila y columna del nodo.
                y, x = click_p

                y = y - PADDING / 2
                x = x - PADDING / 2

                row = y // interval
                col = x // interval
                x,y = int(col), int(row)

                if prev_x and prev_y:
                    grid[prev_x][prev_y].selected = False
                
                if not grid[x][y].selected:
                    grid[x][y].selected = True

                prev_x, prev_y = x,y

                # Si hay una ficha capturada se coloca en la casilla seleccionada.
                if captured_piece:

                    

                    # Se convierte la casilla a formato chess.
                    square = chess.parse_square(node)
                    if not board.piece_at(square):
                        # Se convierte la pieza a formato chess.
                        new_piece = chess.Piece(captured_piece.piece_type, not captured_piece.color)
                        # Se coloca la pieza en la casilla seleccionada.
                        board.set_piece_at(square, new_piece)
                        # Reiniciamos la variable de pieza capturada.
                        captured_piece = None
                        
                        # Sigue la IA.
                        ia_turn(window, grid, width)
                        movement = ""
                    else:
                        
                        print("There is a piece in this square, please try put in other square.")
                else:
                    # Si movement es una cadena vacía, significa que el jugador aún
                    # no ha seleccionado ninguna pieza para mover.
                    if movement == "":
                        # Obtenemos la pieza seleccionada.
                        piece = board.piece_at(chess.Square(chess.parse_square(node)))

                        # Si la pieza es válida, la asignamos al movimiento.
                        if piece is not None and str(piece).isupper():
                            movement = node
                        else:
                            print("Not Valid")

                    # Si movement no es una cadena vacía y es igual al nodo seleccionado,
                    # significa que el jugador ha hecho clic nuevamente en la misma pieza
                    # para cancelar la selección.
                    elif movement == node:
                        movement = ""

                    # Si movement no es una cadena vacía y es diferente del nodo seleccionado,
                    # significa que el jugador ha seleccionado un nodo de destino para su movimiento.
                    else:
                        # Agregamos el nodo al final de la cadena movement.
                        movement += node

                        # Realizamos el movimiento.
                        move = chess.Move.from_uci(movement)

                        # Verificamos si el movimiento no es válido.
                        if move not in board.legal_moves:
                            print('Not valid move')
                            movement = ''

                        # Si es válido, realizamos el movimiento y actualizamos el tablero.
                        else:
                            if board.is_capture(move):
                                captured_piece = board.piece_at(chess.Square(chess.parse_square(node)))
                                print(f"Captured: {captured_piece}")

                            board.push(chess.Move.from_uci(movement))
                            movement = ""

                            if not captured_piece:
                                # Sigue la IA.
                                IA_turn(window, grid, width)
                                movement = ""
            
            update_display(window, grid, 8, width, 0)
            
            #grid = make_grid(8, width)
            
def get_node_position(node, width):
    """
    Obtiene las coordenadas en píxeles de un nodo en la ventana.

    node: nodo del tablero de ajedrez.
    width: ancho total de la ventana.
    """
    interval = width / 8
    x = node.col * interval
    y = node.row * interval
    return int(x), int(y)        


def IA_turn(window, grid, width):
    # Actualizar el tablero y sigue la IA.
    
    update_display(window, grid, 8, width, 1)
    # Después del turno del jugador, indicamos que es turno de la IA.
    pygame.display.set_caption("Crazy Chess | IA turn")
    # Realizamos una copia del tablero para evaluar si hay captura y obtener la ficha capturada.
    board_copy = board.copy()

    # La máquina selecciona el movimiento a hacer.
    movement = machine_move(board_copy)
    # Realiza el movimiento.
    board.push(chess.Move.from_uci(movement))

    is_capture = board_copy.is_capture(chess.Move.from_uci(movement))
    if is_capture:
        # Actualizar el tablero y coloca la ficha.
        update_display(window, grid, 8, width)
        captured_piece_square = movement[-2:]
        captured_piece = board_copy.piece_at(chess.Square(chess.parse_square(captured_piece_square)))
        print(f"Captured: {captured_piece}")
        square = put_piece(board.copy(), captured_piece)
        # Se convierte la pieza a formato chess.
        piece = chess.Piece(captured_piece.piece_type, not captured_piece.color)
        # Se coloca la pieza en la casilla seleccionada.
        board.set_piece_at(square, piece)

# Ejecutamos el juego.
main(WIN, WIDTH)