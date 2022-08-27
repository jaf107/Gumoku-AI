import pygame

from board import Board
from player import Player
from engine import Engine


class Game:
    def __init__(self, board: Board):
        self.grid_size = 30
        self.start_x, self.start_y = 30, 50
        self.edge_size = self.grid_size // 2

        self.board = board
        self.last_move = None

        self.black_turn = True
        self.game_over = False
        self.winner = 0

        self.black_score = 0
        self.white_score = 0

    def handle_key_event(self, e):  # Comes from User
        origin_x = self.start_x - self.edge_size
        origin_y = self.start_y - self.edge_size
        size = (self.board.size - 1) * self.grid_size + self.edge_size * 2
        pos = e.pos
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            x = pos[0] - origin_x
            y = pos[1] - origin_y
            row = int(y // self.grid_size)
            col = int(x // self.grid_size)
            self.set_piece(row, col)
        self.black_turn = not self.black_turn

    def ai_play(self):
        row, col = Engine.find_next_move(self.board, 3)
        self.set_piece(row, col)
        self.black_turn = not self.black_turn

    def set_piece(self, row, col):
        if self.board.matrix[row][col] == 0:
            if self.black_turn:
                self.board.matrix[row][col] = Player.BLACK   
            else:
                self.board.matrix[row][col] = Player.WHITE
                
            self.last_move = (row, col)
            return True
        return False

    def check_win(self):
        if self.board.check_win(1):
            self.winner = 1
            self.game_over = True
        if self.board.check_win(2):
            self.winner = 2
            self.game_over = True

    def draw(self, screen):
        pygame.draw.rect(screen, (205, 128, 0), [self.start_x - self.edge_size, self.start_y - self.edge_size, (self.board.size - 1)
                                                  * self.grid_size + self.edge_size * 2, (self.board.size - 1) * self.grid_size + self.edge_size * 2], 0)

        for r in range(self.board.size):
            y = self.start_y + r * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [self.start_x, y], [
                             self.start_x + self.grid_size * (self.board.size - 1), y], 2)

        for c in range(self.board.size):
            x = self.start_x + c * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [x, self.start_y], [
                             x, self.start_y + self.grid_size * (self.board.size - 1)], 2)

        for r in range(self.board.size):
            for c in range(self.board.size):
                piece = self.board.matrix[r][c]
                if piece != 0:
                    if piece == 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)

                    x = self.start_x + c * self.grid_size
                    y = self.start_y + r * self.grid_size
                    pygame.draw.circle(screen, color, [x, y], self.grid_size // 2)

        if self.last_move:
            y, x = self.last_move
            x = self.start_x + x * self.grid_size
            y = self.start_y + y * self.grid_size
            color = (255, 0, 0)
            pygame.draw.circle(screen, color, [x, y], self.grid_size // 4)
