import random
import math
from copy import deepcopy
import random

RED = (255, 0, 0)
BLUE = (0, 0, 255)

def selection(population):
    maxEval = float('-inf')
    best_move = None
    for pos in population:
        evaluation = pos.evaluate()
        maxEval = max(maxEval, evaluation)
        if maxEval == evaluation:
            best_move = pos
    return maxEval, best_move


def genetic_algorithm(position, generation, game):
    if position.winner() != None:
        return position.evaluate(),position
    population = get_all_moves(position, BLUE, game)
    value,best_move = selection(population)
    return value,best_move
        
        
    
def simulate_move(piece, move, board, game, skipped):
    board.move(piece, move[0], move[1])
    if (skipped[(move[0], move[1])] != 0):
        (r, c) = skipped[move[0], move[1]]
        piece = board.get_piece(r, c)
        board.remove(piece)
    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        [valid_moves, skipped, catch] = board.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skipped)
            moves.append(new_board)
    return moves
