import chess
import math

from utils import PIECE_VALUES, POSITION_VALUES



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



def min_max_max(board, movement, depth):
    """
    Implementa el algoritmo Minimax para la búsqueda del mejor movimiento.
    Esta función busca el movimiento que maximiza el valor de evaluación en
    un nivel determinado del árbol de búsqueda.

        board : estado del tablero.
        movement : movimiento actual.
        depth : profundidad actual de la búsqueda.
    """
    # Si la profundidad es menor a 0, se alcanzó el nivel máximo de profundidad.
    if depth < 0:
        value = evaluate_board(board, movement)

        return {
            "value": value,
            "movement": movement
        }

    # Aplicamos el movimiento al tablero actual.
    board.push(chess.Move.from_uci(movement))

    # Inicializamos la variable como -Infinite.
    maximum = -(math.inf)

    # Obtenemos todas las jugadas legales disponibles en el tablero.
    legal_moves = [str(mov) for mov in board.legal_moves]

    result = {}

    # Para cada movimiento legal obtenemos aquel con la mayor puntuación.
    for move in legal_moves:
       evaluation = min_max_min(board.copy(), move, depth-1)

       if  evaluation["value"] > maximum:
            maximum = evaluation["value"]
            result = evaluation

    return result



def min_max_min(board, movement, depth):
    """
    Implementa el algoritmo Minimax para la búsqueda del mejor movimiento.
    Esta función busca el movimiento que minimiza el valor de evaluación en
    un nivel determinado del árbol de búsqueda.

        board : estado del tablero.
        movement : movimiento actual.
        depth : profundidad actual de la búsqueda.
    """
    # Si la profundidad es menor a 0, se alcanzó el nivel máximo de profundidad.
    if depth < 0:
        value = evaluate_board(board, movement)

        return {
            "value": value,
            "movement": movement
        }

    # Aplicamos el movimiento al tablero actual.
    board.push(chess.Move.from_uci(movement))

    # Inicializamos la variable como +Infinite.
    minimum = math.inf

    # Obtenemos todas las jugadas legales disponibles en el tablero.
    legal_moves = [str(mov) for mov in board.legal_moves]

    result = {}

    # Para cada movimiento legal obtenemos aquel con la menor puntuación.
    for move in legal_moves:
       evaluation = min_max_max(board.copy(), move, depth-1)

       if  evaluation["Value"] < minimum:
            minimum = evaluation["Value"]
            result = evaluation

    return result