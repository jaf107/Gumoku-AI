from tkinter import *
from tkinter import ttk
import pygame


# IMPORTS
from board import Board
from engine import Engine
from game import Game

class GomokuUI():
    

    def __init__(self, name="Gomoku", size=12 ):
        pygame.init()
        pygame.display.set_caption(name)
        self.width = 30 * size + 30
        self.height = 30 * size + 30 + 150
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 24)
        self.board = Board(size=size)

        # self.mode = mode
        self.going = True
        self.clock = pygame.time.Clock()
        self.game = Game(self.board)

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

    def restartBox(self):
            # Create an instance of tkinter frame
        win = Tk()

        # Define a function to implement choice function
        def choice(option):
            pop.destroy()
            if option == "yes":
                pygame.quit()
            else:
                return
        global pop
        pop = win
        pop.title("Confirmation")
        pop.geometry("350x200")
        pop.config(bg="white")
        # Create a Label Text
        label = Label(pop, text="Winner is Black" if self.game.winner == 2 else "Winner is White",
        font=('Aerial', 12))
        label.pack(pady=20)
        label = Label(pop, text="Would You like to Quit?",
        font=('Aerial', 12))
        label.pack(pady=20)
        # Add a Frame
        frame = Frame(pop, bg="gray71")
        frame.pack(pady=10)
        # Add Button for making selection
        button1 = Button(frame, text="Yes", command=lambda: choice("yes"), bg="blue", fg="white")
        button1.grid(row=0, column=1)
        button2 = Button(frame, text="No", command=lambda: choice("no"), bg="blue", fg="white")
        button2.grid(row=0, column=2)
        win.mainloop()


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.font.render("Turn: {0}".format("Black" if self.game.black_turn else "White"), True, (0, 0, 0)), (10, self.height - 125))

        self.game.draw(self.screen)
        if self.game.game_over:
            self.screen.blit(self.font.render("{0} Win".format("Black" if self.game.winner == 2 else "White"), True, (0, 0, 0)), (self.width // 4 * 3, 10))
            self.restartBox()

        pygame.display.update()


if __name__ == '__main__':
    game = GomokuUI("Gomoku", 12)
    game.loop()
