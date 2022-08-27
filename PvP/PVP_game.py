from turtle import Screen, circle
import numpy as np
import pygame 
import sys
import math

# initialize pygame program 
pygame.init()

# static variables 
ROW_COUNT = 10
COL_COUNT = 10

# screen size 
BLOCKSIZE = 50
S_WIDTH = COL_COUNT * BLOCKSIZE
S_HEIGHT = ROW_COUNT * BLOCKSIZE
PADDING_RIGHT = 0
SCREENSIZE = (S_WIDTH + PADDING_RIGHT, S_HEIGHT)
RADIUS = 20

# colors 
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BROWN = (205, 128, 0)

#  create a board array 
def create_board(row, col):
    board = np.zeros((row, col))
    return board

# draw a board in pygame window 
def draw_board(screen):
    
    # basic board layout 
    for x in range(0, S_WIDTH, BLOCKSIZE):
        for y in range(0, S_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BROWN, rect)
            
    # INNER GRID LINES 

    # vertical lines
    for x in range(BLOCKSIZE // 2, S_WIDTH - BLOCKSIZE // 2 + BLOCKSIZE, BLOCKSIZE):
        line_start = (x, BLOCKSIZE // 2)
        line_end = (x, S_HEIGHT - BLOCKSIZE // 2)
        pygame.draw.line(screen, BLACK, line_start, line_end, 2) 
    
    # vertical lines 
    for y in range(BLOCKSIZE // 2, S_HEIGHT - BLOCKSIZE // 2 + BLOCKSIZE, BLOCKSIZE):
        line_start = (BLOCKSIZE // 2, y)
        line_end = (S_WIDTH - BLOCKSIZE // 2, y)
        pygame.draw.line(screen, BLACK, line_start, line_end, 2) 
    
    
        
    pygame.display.update()

def drop_piece(board, row, col, piece):
    board[row][col] = piece
    
def draw_piece(screen, board):
    # draw game pieces at mouse pressed location 
    for x in range(COL_COUNT):
        for y in range(ROW_COUNT):
            circle_pos = ( x * BLOCKSIZE + BLOCKSIZE//2, y * BLOCKSIZE + BLOCKSIZE//2 )
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, circle_pos, RADIUS)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, WHITE, circle_pos, RADIUS)
    pygame.display.update()


# check for a valid location 
def valid_loc(board, row, col):
    return board[row][col] == 0

def who_wins(board, piece):
    # check for horizontal win
    for c in range(COL_COUNT - 4):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece\
                and board[r][c+4] == piece:
                return True
            
            # winCase = True
            # for i in range(5):
            #     if board[r][c+i] != piece:
            #         winCase = False
    
    #  check for vertical win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 4):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece\
                and board[r+4][c] == piece:
                    return True
                
    # check for positive slope diagonal 
    for c in range(COL_COUNT-4):
        for r in range(4,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece\
                and board[r-4][c+4] == piece:
                return True

    # check for negatively sloped diagonal win
    for c in range(COL_COUNT-4):
        for r in range(ROW_COUNT-4):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece\
                and board[r+4][c+4] == piece:
                return True
                    
def main():
    
    game_over = False
    turn  = 0
    piece_1 = 1
    piece_2 = 2
    
    FPS = 60
    frames_per_sec = pygame.time.Clock()
    
    board = create_board(ROW_COUNT, COL_COUNT)
    print(board)
    
    SCREEN = pygame.display.set_mode(SCREENSIZE)
    SCREEN.fill(WHITE)
    pygame.display.set_caption('Gomoku (Connect 5)')
    
    # font
    my_font = pygame.font.Font('freesansbold.ttf', 32)

    # text message
    label_1 = my_font.render('Black wins!', True, WHITE, BLACK)
    label_2 = my_font.render('White wins!', True, WHITE, BLACK)
    
    # display the Screen
    draw_board(SCREEN)
    while not game_over:
        
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                y_pos = event.pos[1]
                
                col = int(math.floor(x_pos / BLOCKSIZE))
                row = int(math.floor(y_pos / BLOCKSIZE))
                
                if board[row][col] == 1:
                    turn = 0
                if board[row][col] == 2:
                    turn = 1
                    
                if turn == 0:
                    if valid_loc(board, row, col):
                        drop_piece(board, row, col, piece_1)
                        draw_piece(SCREEN, board)
                        
                        if who_wins(board, piece_1):
                            print('Black wins!')
                            SCREEN.blit(label_1, (280,50))
                            pygame.display.update()
                            game_over = True
                            
                else:
                    if valid_loc(board, row, col):
                        drop_piece(board, row, col, piece_2)
                        draw_piece(SCREEN, board)
                        
                        if who_wins(board, piece_2):
                            print('White wins!')
                            SCREEN.blit(label_2, (280,50))
                            pygame.display.update()
                            game_over = True
                
                print(board)
                
                turn += 1
                turn = turn %2
                
                if game_over:
                    pygame.time.wait(3000)
        
        frames_per_sec.tick(FPS)
        
if __name__ == '__main__':
    main()