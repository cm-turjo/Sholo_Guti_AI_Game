import pygame
from board import Board
from constant import RED , BLUE ,GREEN ,SQUARE_SIZE,COLS,ROWS
from fuzzy_logic import fuzzy

class Game:
    def __init__(self,win):
        self._init()
        self.win = win
        self.no_of_moves = 0

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        move_TEXTb = pygame.font.SysFont('Consolas',14).render(f"TOTAL MOVES:{self.no_of_moves}", True, "black")
        move_RECTb = move_TEXTb.get_rect(center=(205, 20))
        self.win.blit(move_TEXTb, move_RECTb)

        PLAY_TEXTb = pygame.font.SysFont('Consolas',14).render(f"HUMAN:{self.board.red_left}", True, "red")
        PLAY_RECTb = PLAY_TEXTb.get_rect(center=(50, 740))
        self.win.blit(PLAY_TEXTb, PLAY_RECTb)
        PLAY_TEXTr = pygame.font.SysFont('Consolas',14).render(f"AI:{self.board.blue_left}", True, "blue")
        PLAY_RECTr = PLAY_TEXTr.get_rect(center=(350, 740))
        self.win.blit(PLAY_TEXTr, PLAY_RECTr)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = []
        self.skipped = []

    def reset(self):
        self._init()


    def select(self, row, col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)
        piece = self.board.get_piece(row,col)
        if piece !=0 and piece !=-1 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves, self.skipped ,_ = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self,row,col):
        piece = self.board.get_piece(row,col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            self.board.move(self.selected, row,col)
            if(self.skipped[(row,col)]!=0):
                (r,c) = self.skipped[(row,col)]
                piece = self.board.get_piece(r, c)
                self.board.remove(piece)

            if (self.skipped[(row, col)] != 0):
                piece = self.board.get_piece(row, col)
                _, _, catch = self.board.get_valid_moves(piece)
                if catch==0:
                    self.change_turn()
            else:
                self.change_turn()
        else:
            return False
        
        self.no_of_moves+=1
        return True

    def draw_valid_moves(self,moves):
        for move in moves:
            col, row = move[0], move[1]
            pygame.draw.circle(self.win,GREEN, (row*SQUARE_SIZE + SQUARE_SIZE//2, col*SQUARE_SIZE + SQUARE_SIZE//2),7)


    def change_turn(self):
        self.valid_moves = []
        if self.turn == RED:
            self.turn = BLUE
        else:
            self.turn = RED

    def winner(self):
        return self.board.winner()
    
    def get_standard_of_wining(self):
        remain = abs(self.board.evaluate())
        val = fuzzy(self.no_of_moves, remain)
        return val

    def get_board(self):
        return self.board

    def ai_move(self,board):
        self.board = board
        self.change_turn()

