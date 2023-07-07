import chess
import math

from utils import PIECE_VALUES, POSITION_VALUES

# ============================================================
#              MOVIMIENTOS ESTÁNDAR DE LAS FICHAS
# ============================================================

def machine_move(board):
    """
    Realiza el movimiento por parte de la máquina.

        board : tablero de ajedrez.
    """
    maximum = -(math.inf)
    movement = ""

    # Obtenemos todos los movimientos legales disponibles en el tablero.
    legal_moves = [str(mov) for mov in board.legal_moves]

    # Para cada movimiento legal se realiza la poda alpha-beta con una profundidad
    # máxima de 3 y un indicador False para señalar que es el turno de la máquina.
    for move in legal_moves:
        result = alphabeta_pruning(board.copy(), move, 3, -(math.inf), math.inf, False)

        # Se busca que el movimiento tenga el máximo valor.
        if result > maximum:
            movement = move
            maximum = result

    return movement


def alphabeta_pruning(board, movement, depth, alpha, beta, maximizing_player):
    """
    Implementa la poda alpha-beta.

        board : estado actual del tablero.
        movement : movimiento actual.
        depth : profundidad actual del árbol de búsqueda.
        alpha : valor alfa.
        beta : valor beta.
        maximizing_player : indicador que especifica si el jugador actual está
                            maximizando o minimizando.
    """
    # Verificamos si hemos alcanzado la profundidad máxima de búsqueda.
    if depth == 0:
        return evaluate_board(board, movement)

    # Aplicamos el movimiento actual al tablero utilizado.
    board.push(chess.Move.from_uci(movement))

    # Obtenemos todos los movimientos legales disponibles para el estado actual del tablero.
    legal_moves = [str(mov) for mov in board.legal_moves]

    # Si el jugador en el nivel actual del árbol es el jugador maximizador,
    # se realiza una búsqueda maximizadora.
    if maximizing_player:
        # Inicializamos value como -Infinite.
        value = -(math.inf)

        # Para cada movimiento se reliza una llamada recursiva de alphabeta_pruning()
        # con una profundidad reducida de 1 y se invierte el valor de maximizing_player.
        for move in legal_moves:
            value = max(value, alphabeta_pruning(board.copy(), move, depth-1, alpha, beta, False))

            # Si value es mayor o igual a beta, se realiza el corte beta y se sale del bucle,
            # ya que se ha encontrado un valor que el jugador minimizador no permitiría.
            if value >= beta:
                break

            alpha = max(alpha, value)

        return value

    # Si no, se realiza una búsqueda minimizadora.
    else:
        # Inicializamos value como +Infinite.
        value = (math.inf)

        for move in legal_moves:
            value = min(value, alphabeta_pruning(board.copy(), move, depth-1, alpha, beta, True))

            # Si value es menor o igual que alpha se realiza el corte alpha y se sale del bucle.
            if value <= alpha:
                break

            beta = min(beta, value)

        return value



def evaluate_board(board, movement):
    """
    Evalúa el estado del tablero en función de los valores asignados a las
    piezas y las posiciones.

        board : estado del tablero.
        movement : movimiento actual.
    """
    # Creamos un acumulador para la puntuación de la evaluación.
    value = 0

    # Aplicamos el movimiento actual al tablero.
    board.push(chess.Move.from_uci(movement))

    # Recorremos todas las casillas del tablero.
    for i in range(8):
        for j in range(8):
            # Para cada casilla obtenemos la pieza en esa posición.
            piece = str(board.piece_at(chess.Square((i * 8 + j))))

            # Obtenemos el valor asignado a la pieza.
            # Si no hay pieza en esa casilla, se asigna un valor de 0.
            piece_val = PIECE_VALUES[piece] if piece != 'None' else 0

            # Obtenemos el valor asignado a la posición de la pieza.
            pos_val = POSITION_VALUES[piece][i][j] if piece != 'None' else 0

            value += piece_val + pos_val

    return value

# ============================================================
#                 POSICIONAR FICHAS ROBADAS
# ============================================================
def put_piece(board, piece):
    """
    Coloca la ficha robada por parte de la máquina.
        board : tablero de ajedrez.
    """
    maximum = -(math.inf)
    movement = ""

    # Determina las coordenadas de la cuadrícula central 4x4
    start_row = 2
    end_row = 6
    start_col = 2
    end_col = 6

    # Obtiene las casillas vacías en la cuadrícula central
    # empty_squares = []
    # for row in range(start_row, end_row + 1):
    #     for col in range(start_col, end_col + 1):
    #         square = chess.square(col, row)
    #         if board.piece_at(square) is None:
    #             empty_squares.append(square)

    # Obtenemos las casillas que están vacías en el tablero.
    empty_squares = [square for square in chess.SQUARES if board.piece_at(square) is None]

    # Para cada movimiento legal realiza la poda alpha-beta con una profundidad
    # máxima de 3 y un indicador False para señalar que es el turno de la máquina.
    for square in empty_squares:
        result = alphabeta_pruning_alt(board.copy(), piece, square, 3, -(math.inf), math.inf, False)

        # Busca el movimiento con el máximo valor.
        if result > maximum:
            movement = square
            maximum = result

    return movement


def alphabeta_pruning_alt(board, piece, square, depth, alpha, beta, maximizing_player):
    """
    Implementa la poda alpha-beta.

        board : estado actual del tablero.
        square : casilla actual.
        depth : profundidad actual del árbol de búsqueda.
        alpha : valor alfa.
        beta : valor beta.
        maximizing_player : indicador que especifica si el jugador actual está
                            maximizando o minimizando.
    """
    # Verificamos si hemos alcanzado la profundidad máxima de búsqueda.
    if depth == 0:
        return evaluate_board_alt(board, square, piece)

    # TODO: Colocar la ficha.board.push(chess.Move.from_uci(movement))
    # Se convierte la pieza a formato chess.
    piece = chess.Piece(piece.piece_type, not piece.color)
    # Se coloca la pieza en la casilla seleccionada.
    board.set_piece_at(square, piece)

    # Obtenemos las casillas que están vacías en el tablero.
    empty_squares = [square for square in chess.SQUARES if board.piece_at(square) is None]

    # Si el jugador en el nivel actual del árbol es el jugador maximizador,
    # se realiza una búsqueda maximizadora.
    if maximizing_player:
        # Inicializamos value como -Infinite.
        value = -(math.inf)

        # Para cada movimiento se reliza una llamada recursiva de alphabeta_pruning()
        # con una profundidad reducida de 1 y se invierte el valor de maximizing_player.
        for square in empty_squares:
            value = max(value, alphabeta_pruning_alt(board.copy(), piece, square, depth-1, -(math.inf), math.inf, False))

            # Si value es mayor o igual a beta, se realiza el corte beta y se sale del bucle,
            # ya que se ha encontrado un valor que el jugador minimizador no permitiría.
            if value >= beta:
                break

            alpha = max(alpha, value)

        return value

    # Si no, se realiza una búsqueda minimizadora.
    else:
        # Inicializamos value como +Infinite.
        value = (math.inf)

        for square in empty_squares:
            value = max(value, alphabeta_pruning_alt(board.copy(), piece, square, depth-1, -(math.inf), math.inf, True))

            # Si value es menor o igual que alpha se realiza el corte alpha y se sale del bucle.
            if value <= alpha:
                break

            beta = min(beta, value)

        return value


def evaluate_board_alt(board, square, piece):
    """
    Evalúa el estado del tablero en función de los valores asignados a las
    piezas y las posiciones.

        board : estado del tablero.
        movement : movimiento actual.
    """
    # Creamos un acumulador para la puntuación de la evaluación.
    value = 0

    # Se convierte la pieza a formato chess.
    piece = chess.Piece(piece.piece_type, not piece.color)
    # Se coloca la pieza en la casilla seleccionada.
    board.set_piece_at(square, piece)

    # Recorremos todas las casillas del tablero.
    for i in range(8):
        for j in range(8):
            # Para cada casilla obtenemos la pieza en esa posición.
            piece = str(board.piece_at(chess.Square((i * 8 + j))))

            # Obtenemos el valor asignado a la pieza.
            # Si no hay pieza en esa casilla, se asigna un valor de 0.
            piece_val = PIECE_VALUES[piece] if piece != 'None' else 0

            # Obtenemos el valor asignado a la posición de la pieza.
            pos_val = POSITION_VALUES[piece][i][j] if piece != 'None' else 0

            value += piece_val + pos_val

    return value