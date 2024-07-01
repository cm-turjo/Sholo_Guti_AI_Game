from copy import deepcopy
import  pygame
RED = (255,0,0)
BLUE = (0,0,255)

def alphabeta_pruning(position, depth, max_player, game, alpha ,beta):
    if depth==0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLUE , game):
            evaluation = alphabeta_pruning(move,depth-1,False,game,alpha,beta)[0]
            maxEval = max(maxEval, evaluation)
            # alpha = max(alpha,maxEval)
            # if beta <= alpha:
            #     break
            # if maxEval == evaluation:
            #     best_move = move
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break 
            
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = alphabeta_pruning(move, depth - 1, True, game,alpha,beta)[0]
            minEval = min(minEval, evaluation)
            # beta = min(beta,minEval)
            # if beta <= alpha:
            #     break
            # if minEval == evaluation:
            #     best_move = move
            if minEval == evaluation:
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return minEval, best_move



def simulate_move(piece, move ,board, game ,skipped):
    board.move(piece,move[0],move[1])

    if (skipped[(move[0], move[1])] != 0):
        (r, c) = skipped[move[0], move[1]]
        piece = board.get_piece(r, c)
        board.remove(piece)
    return board

def get_all_moves(board, color , game):
    moves = []
    for piece in board.get_all_pieces(color):
        [valid_moves, skipped, catch] = board.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece,move,temp_board,game,skipped)
            moves.append(new_board)

    return moves




