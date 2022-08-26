import time
import math

import numpy as np
import pygame


class Player:
    WHITE = 1 # Computer
    BLACK = 2 # Human


class Board: 
    def __init__(self, board=None, matrix=None, size=None):
        if board is not None:
            self.matrix = np.array(board.matrix)
        if matrix is not None:
            self.matrix = np.array(matrix)
        if size is not None:
            self.matrix = np.zeros((size, size))
        self.size = self.matrix.shape[0]

    def __check_row(self, color):
        neg_color = 1 if color == 2 else 2
        for i in range(self.size):
            for j in range(self.size-4):
                window = self.matrix[i, j:j+5]
                if np.equal(window, np.ones(5) * color).all():
                    if 0 <= j-1 and j+5 < self.size:
                        if self.matrix[i, j-1] == neg_color and self.matrix[i, j+5] == neg_color:
                            continue
                    return True
        return False

    def __check_col(self, color):
        neg_color = 1 if color == 2 else 2
        for i in range(self.size-4):
            for j in range(self.size):
                window = self.matrix[i:i+5, j]
                if np.equal(window, np.ones(5) * color).all():
                    if 0 <= i-1 and i+5 < self.size:
                        if self.matrix[i-1, j] == neg_color and self.matrix[i+5, j] == neg_color:
                            continue
                    return True
        return False

    def __check_diagonal(self, color):
        neg_color = 1 if color == 2 else 2
        for i in range(self.size-4):
            for j in range(self.size-4):
                window = self.matrix[i:i+5, j:j+5]
                if np.equal(window.diagonal(), np.ones(5) * color).all():
                    if 0 <= i-1 and i+5 < self.size and 0 < j-1 and j+5 < self.size:
                        if self.matrix[i-1, j-1] == neg_color and self.matrix[i+5, j+5] == neg_color:
                            continue
                    return True
                if np.equal(np.fliplr(window).diagonal(), np.ones(5) * color).all():
                    if 0 <= i-1 and i+5 < self.size and 0 < j-1 and j+5 < self.size:
                        if self.matrix[i-1, j+5] == neg_color and self.matrix[i+5, j-1] == neg_color:
                            continue
                    return True
        return False

    def check_win(self, color):
        if self.__check_row(color):
            return True
        if self.__check_col(color):
            return True
        if self.__check_diagonal(color):
            return True
        return False

    def generate_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i, j] > 0:
                    continue
                # moves.append((i, j))
                if i > 0:
                    if j > 0:
                        if self.matrix[i-1][j-1] > 0 or self.matrix[i][j-1] > 0:
                            moves.append((i, j))
                            continue
                    if j < self.size - 1:
                        if self.matrix[i-1][j+1] > 0 or self.matrix[i][j+1] > 0:
                            moves.append((i, j))
                            continue
                    if self.matrix[i-1][j] > 0:
                        moves.append((i, j))
                        continue
                if i < self.size - 1:
                    if j > 0:
                        if self.matrix[i+1][j-1] > 0 or self.matrix[i][j-1] > 0:
                            moves.append((i, j))
                            continue
                    if j < self.size - 1:
                        if self.matrix[i+1][j+1] > 0 or self.matrix[i][j+1] > 0:
                            moves.append((i, j))
                            continue
                    if self.matrix[i+1][j] > 0:
                        moves.append((i, j))
                        continue
        return moves

    def draw(self, move, is_black):
        if is_black:
            color = Player.BLACK
        else:
            color = Player.WHITE
        
        self.matrix[move] = color



class Engine:
    evaluation_count = 0
    calculation_time = 0

    @classmethod
    def __get_patterns(cls, line, pattern_dict, is_black):
        color = 2 if is_black else 1
        neg_color = 1 if is_black else 2
        s = ''
        old = 0

        for i, c in enumerate(line):
            if i == 0:
                s += 'O'
            if c == color:
                if old == neg_color:
                    s += 'O'
                s += 'X'
            if c != color or i == len(line)-1:
                if c == neg_color and len(s) > 0:
                    s += 'O'
                elif i == len(line)-1:
                    s += 'O'
                if s in pattern_dict.keys():
                    pattern_dict[s] += 1
                else:
                    pattern_dict[s] = 1
                s = ''
            old = c

    @classmethod
    def __get_patterns_row(cls, board: Board, pattern_dict, is_black):
        size = board.size
        matrix = board.matrix
        for i in range(size):
            cls.__get_patterns(matrix[i], pattern_dict, is_black)

    @classmethod
    def __get_patterns_col(cls, board: Board, pattern_dict, is_black):
        size = board.size
        matrix = board.matrix
        for i in range(size):
            cls.__get_patterns(matrix[:, i], pattern_dict, is_black)

    @classmethod
    def __get_patterns_diagonal(cls, board: Board, pattern_dict, is_black):
        size = board.size
        matrix1 = board.matrix
        matrix2 = matrix1[::-1, :]
        for i in range(-size+1, size):
            cls.__get_patterns(matrix1.diagonal(i), pattern_dict, is_black)
            cls.__get_patterns(matrix2.diagonal(i), pattern_dict, is_black)

    @classmethod
    def evaluate_board(cls, board: Board, is_black_turn: bool):
        cls.evaluation_count += 1
        black_score = cls.get_score(board, True, is_black_turn)
        white_score = cls.get_score(board, False, is_black_turn)
        if black_score == 0: 
            black_score = 1.0
        return white_score / black_score

    @classmethod
    def get_score(cls, board: Board, is_black: bool, is_black_turn: bool):
        pattern_dict = {}
        cls.__get_patterns_row(board, pattern_dict, is_black)
        cls.__get_patterns_col(board, pattern_dict, is_black)
        cls.__get_patterns_diagonal(board, pattern_dict, is_black)
        return cls.get_consecutive_score(pattern_dict)

    @classmethod
    def get_consecutive_score(cls, pattern_dict):
        score = 0
        print(pattern_dict)
        for pattern in pattern_dict:
            if pattern.count('X') == 5:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                else:
                    score += 100000
            if pattern.count('X') == 4:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 5000 * pattern_dict[pattern]
                else:
                    score += 10000 * pattern_dict[pattern]
            if pattern.count('X') == 3:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 500 * pattern_dict[pattern]
                else:
                    score += 1000 * pattern_dict[pattern]
            if pattern.count('X') == 2:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 50 * pattern_dict[pattern]
                else:
                    score += 100 * pattern_dict[pattern]
            if pattern.count('X') == 1:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                else:
                    score += 1 * pattern_dict[pattern]
        return score

    @classmethod
    def find_next_move(cls, board: Board, depth):
        cls.evaluation_count = 0
        cls.calculation_time = 0

        start = time.time()
        
        value, best_move = cls.__search_winning_move(board)
        if best_move is not None:
            move = best_move
        else:
            value, best_move = cls.minimax_alphabeta(board, depth, -1.0, 100000000, True)
            if best_move is None:
                move = None
            else:
                move = best_move
        end = time.time()
        cls.calculation_time = end-start
        if move is None:
            move = (board.size//2, board.size//2)
        return move


    # NEED TO BE UNDERSTOOD
    @classmethod
    def heuristic_sort(cls, board, all_moves):
        def my_func(board, move):
            x, y = move
            count = 0
            size = board.size
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if 0 <= x+i < size and 0 <= y+j < size:
                        if board.matrix[x+i][y+j] != 0:
                            count += 1
            return count

        return sorted(all_moves, key=lambda move: my_func(board, move), reverse=True)

    @classmethod
    def minimax_alphabeta(cls, board: Board, depth, alpha, beta, is_max):
        if depth == 0:
            return (cls.evaluate_board(board, not is_max), None)

        all_possible_moves = board.generate_moves()
        all_possible_moves = cls.heuristic_sort(board, all_possible_moves)

        if len(all_possible_moves) == 0:
            return (cls.evaluate_board(board, not is_max), None)

        best_move = None

        if is_max: # Max Node
            best_value = -math.inf
            for move in all_possible_moves:
                dumm_board = Board(board=board)
                dumm_board.draw(move, False) # 
                value, temp_move = cls.minimax_alphabeta(dumm_board, depth-1, alpha, beta, not is_max)
                if value > alpha:
                    alpha = value
                if value >= beta:
                    return (value, temp_move)
                if value > best_value:
                    best_value = value
                    best_move = move
        else: # Min Node
            best_value = math.inf
            for move in all_possible_moves:
                dumm_board = Board(board=board)
                dumm_board.draw(move, True)
                value, temp_move = cls.minimax_alphabeta(dumm_board, depth-1, alpha, beta, not is_max)
                if value < beta:
                    beta = value
                if value <= alpha:
                    return (value, temp_move)
                if value < best_value:
                    best_value = value
                    best_move = move
        return (best_value, best_move)

    @classmethod
    def __search_winning_move(cls, board: Board):
        all_possible_moves = board.generate_moves()

        for move in all_possible_moves:
            dumm_board = Board(board=board)
            dumm_board.draw(move, False) # False returns not black
            if dumm_board.check_win(1):
                return (None, move)
            dumm_board = Board(board=board)
            dumm_board.draw(move, True) # True returns is_black
            if dumm_board.check_win(2):
                return (None, move)
        return (None, None)


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


class GomokuUI():
    

    def __init__(self, name="Gomoku", size=12 ):
        pygame.init()
        pygame.display.set_caption(name)
        self.width = 30 * size + 30
        self.height = 30 * size + 30 + 150
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 24)
        board = Board(size=size)

        # self.mode = mode
        self.going = True
        self.clock = pygame.time.Clock()
        self.game = Game(board)

    def loop(self):
        while self.going:
            self.update()
            self.draw()
        pygame.quit()

    def handle_event(self): # Mouse input from User
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.going = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.game.handle_key_event(e)

    def update(self):
        self.game.check_win()
        if self.game.game_over:
            return
        # Player Vs Computer mode always

        if self.game.black_turn: 
            # Player move - (User Input)
            self.handle_event()
        else:
            # Computer move
            self.game.ai_play()

        self.game.black_score = Engine.get_score(self.game.board, True, not self.game.black_turn)
        self.game.white_score = Engine.get_score(self.game.board, False, not self.game.black_turn)

    def restartBox():
        self

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.font.render("Turn: {0}".format("Black" if self.game.black_turn else "White"), True, (0, 0, 0)), (10, self.height - 125))

        self.game.draw(self.screen)
        if self.game.game_over:
            self.screen.blit(self.font.render("{0} Win".format("Black" if self.game.winner == 2 else "White"), True, (0, 0, 0)), (self.width // 4 * 3, 10))

        pygame.display.update()


if __name__ == '__main__':
    game = GomokuUI("Gomoku", 12)
    game.loop()
