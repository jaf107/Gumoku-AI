import numpy as np

from player import Player

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
