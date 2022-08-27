import time
import math

from board import Board

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
