import pygame
from dice import Dice
from buttons import Button
from collections import deque

class GridSquare(pygame.sprite.Sprite):
    def __init__(self, i, j, game_board):
        super(GridSquare, self).__init__()
        self.origin = (game_board.origin[0] + i*60, game_board.origin[1] + j*60)
        self.square = pygame.Rect(self.origin[0], self.origin[1], game_board.side_length//7, game_board.side_length//7)
        self.top_face = None
        self.is_permanent = False

    def set_top_face(self, top_face):
        if not self.is_permanent:
            self.top_face = top_face

    def make_top_face_permanent(self):
        self.is_permanent = True



class GameBoard:
    def __init__(self, origin_x, origin_y, side_length):
        self.origin = (origin_x, origin_y)
        self.side_length = side_length
        self.draw_board = pygame.Rect(origin_x, origin_y, self.side_length, self.side_length)
        self.notice_board = pygame.Rect(540, 280, 280, 60)

        self.Buttons = pygame.sprite.Group()
        self.button_types = {"Roll":[560, 680, 67.45, 30],
                             "Undo":[660, 680, 67.5, 30],
                             "Restart":[740, 680, 67, 30],
                             "use1":[640, 375, 50, 30],
                             "use2":[640, 455, 50, 30],
                             "use3":[640, 535, 50, 30],
                             "use4":[640, 615, 50, 30],
                             "rotate1":[700, 375, 50, 30],
                             "rotate2":[700, 455, 50, 30],
                             "rotate3":[700, 535, 50, 30],
                             "rotate4":[700, 615, 50, 30],
                             "mirror1":[760, 375, 50, 30],
                             "mirror2":[760, 455, 50, 30],
                             "mirror3":[760, 535, 50, 30],
                             "mirror4":[760, 615, 50, 30]
        }

        for button_type, button in self.button_types.items():
            self.Buttons.add(Button(button, button_type))

        self.round_number = 0
        self.score = 0

        self.grid_squares = pygame.sprite.Group()
        for i in range(7):
            for j in range(7):
                self.grid_squares.add(GridSquare(i, j, self))

        self.dice = Dice()
        self.stack = deque([])

        self.use_pressed = False
        self.temp_die = None
        self.temp_text = ""
        self.start_time_for_temp_text = None

    def restart_game(self):
        self.round_number = 0
        self.score = 0

        self.grid_squares = pygame.sprite.Group()
        for i in range(7):
            for j in range(7):
                self.grid_squares.add(GridSquare(i, j, self))

        self.dice = Dice()
        self.stack = deque([])

        self.use_pressed = False
        self.temp_die = None


    def get_square_under_mouse(self, x, y):
        for grid_square in self.grid_squares:
            if grid_square.square.collidepoint(x,y):
                return grid_square

        return None


    def get_button_type(self, x, y):
        for button in self.Buttons:
            if button.is_pressed(x,y):
                return button.get_name()

        for grid_square in self.grid_squares:
            if grid_square.square.collidepoint(x,y):
                return "grid_square"


    def grid_square_in_stack(self, grid_square):
        for die, temp_square in self.stack:
            if grid_square == temp_square:
                return True
        return False







