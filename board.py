import pygame
from dice import Dice, SpecialConnection
from buttons import Button
from collections import deque
from loads.load_images import SP_JUNC_1, SP_JUNC_2, SP_JUNC_3, SP_JUNC_4, SP_JUNC_5, SP_JUNC_6

class GridSquare(pygame.sprite.Sprite):
    def __init__(self, i, j, game_board):
        super(GridSquare, self).__init__()
        self.origin = (game_board.origin[0] + i*60, game_board.origin[1] + j*60)
        self.square = pygame.Rect(self.origin[0], self.origin[1], game_board.side_length//7, game_board.side_length//7)
        self.top_face = None
        self.is_permanent = False
        self.used_in_round = None

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
                             "use1":[580, 360, 60, 60],
                             "use2":[580, 440, 60, 60],
                             "use3":[580, 520, 60, 60],
                             "use4":[580, 600, 60, 60],
                             "rotate1":[680, 375, 50, 30],
                             "rotate2":[680, 455, 50, 30],
                             "rotate3":[680, 535, 50, 30],
                             "rotate4":[680, 615, 50, 30],
                             "mirror1":[740, 375, 50, 30],
                             "mirror2":[740, 455, 50, 30],
                             "mirror3":[740, 535, 50, 30],
                             "mirror4":[740, 615, 50, 30],
                             "rotate_special":[520,156,50,20],
                             "score":[660,240,64,30]
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
        self.special_face_selected = None
        self.special_stack = deque([])
        self.special_faces_used = []
        self.special_connections = pygame.sprite.Group()
        self.special_connections_faces = {
            SP_JUNC_1: [40, 140, 60, 60],
            SP_JUNC_2: [120, 140, 60, 60],
            SP_JUNC_3: [200, 140, 60, 60],
            SP_JUNC_4: [280, 140, 60, 60],
            SP_JUNC_5: [360, 140, 60, 60],
            SP_JUNC_6: [440, 140, 60, 60]
        }


        for connection_img, face_param in self.special_connections_faces.items():
            self.special_connections.add(SpecialConnection(connection_img, face_param))

        self.use_pressed = False
        self.temp_die = None
        self.temp_text = ""
        self.start_time_for_temp_text = None
        self.last_actions = deque([])

    def restart_game(self):
        self.round_number = 0
        self.score = 0

        self.grid_squares = pygame.sprite.Group()
        for i in range(7):
            for j in range(7):
                self.grid_squares.add(GridSquare(i, j, self))

        self.dice = Dice()
        self.stack = deque([])
        self.special_face_selected = None
        self.special_stack = deque([])
        self.special_faces_used = []

        self.special_connections = pygame.sprite.Group()
        for connection_img, face_param in self.special_connections_faces.items():
            self.special_connections.add(SpecialConnection(connection_img, face_param))

        self.use_pressed = False
        self.temp_die = None
        self.temp_text = ""
        self.start_time_for_temp_text = None
        self.last_actions = deque([])

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

        for special_face in self.special_connections:
            if special_face.is_selected(x,y):
                return "special_face"


    def grid_square_in_stack(self, grid_square):
        for die, temp_square in self.stack:
            if grid_square == temp_square:
                return True
        return False







