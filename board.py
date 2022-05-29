import pygame
from dice import Dice, SpecialConnection
from buttons import Button
from collections import deque
from loads.load_images import SP_JUNC_1, SP_JUNC_2, SP_JUNC_3, SP_JUNC_4, SP_JUNC_5, SP_JUNC_6
import numpy as np

class GridSquare(pygame.sprite.Sprite):
    def __init__(self, i, j, game_board):
        super(GridSquare, self).__init__()
        self.origin = (game_board.origin[0] + i*60, game_board.origin[1] + j*60)
        self.square = pygame.Rect(self.origin[0], self.origin[1], game_board.side_length//7, game_board.side_length//7)
        self.top_face = None
        self.is_permanent = False
        self.used_in_round = None

        #Changes made are now for the graph to be created
        #conn can be of the following type - Empty, Edge, Rail, Road
        self.left_conn = "Empty"
        self.top_conn = "Empty"
        self.right_conn = "Empty"
        self.bottom_conn = "Empty"

    def set_top_face(self, top_face):
        if not self.is_permanent:
            self.top_face = top_face
            self.set_connections(top_face)

    def make_top_face_permanent(self):
        self.is_permanent = True

    def get_position(self, x, y, game_board):
        return (y - game_board.origin[1])//60, (x - game_board.origin[0])//60

    def get_connections(self):
        return [self.left_conn, self.top_conn, self.right_conn, self.bottom_conn]

    def set_connections_to_None(self):
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = "Empty", "Empty", "Empty", "Empty"

    def get_left_neighbor_conn(self, i,j, game_board):
        if j==0:
            if i == 1:
                return "Rail"
            elif i == 3:
                return "Road"
            elif i == 5:
                return "Rail"
            else:
                return "Edge"
        else:
            return game_board.grid_squares[i][j-1].right_conn

    def get_top_neighbor_conn(self, i,j, game_board):
        if i==0:
            if j == 1:
                return "Road"
            elif j == 3:
                return "Rail"
            elif j == 5:
                return "Road"
            else:
                return "Edge"
        else:
            return game_board.grid_squares[i-1][j].bottom_conn

    def get_right_neighbor_conn(self, i,j, game_board):
        if j==6:
            if i == 1:
                return "Rail"
            elif i == 3:
                return "Road"
            elif i == 5:
                return "Rail"
            else:
                return "Edge"
        else:
            return game_board.grid_squares[i][j+1].left_conn

    def get_bottom_neighbor_conn(self, i,j, game_board):
        if i==6:
            if j == 1:
                return "Road"
            elif j == 3:
                return "Rail"
            elif j == 5:
                return "Road"
            else:
                return "Edge"
        else:
            return game_board.grid_squares[i+1][j].top_conn

    def is_unconnected(self, i, j, game_board):
        left_conn = self.get_left_neighbor_conn(i,j,game_board)
        top_conn = self.get_top_neighbor_conn(i,j,game_board)
        right_conn = self.get_right_neighbor_conn(i,j,game_board)
        bottom_conn = self.get_bottom_neighbor_conn(i,j,game_board)

        return ((left_conn == "Empty") | (left_conn == "Edge")) and \
               ((top_conn == "Empty") | (top_conn == "Edge")) and \
               ((right_conn == "Empty") | (right_conn == "Edge")) and \
               ((bottom_conn == "Empty") | (bottom_conn == "Edge"))

    def match_connection(self, conn1, conn2): #conn2 is the top_face, thus won't have edge
        allowed_connections = [
            ("Empty", "Empty"), ("Empty", "Rail"), ("Empty", "Road"),
            ("Edge", "Empty"), ("Edge", "Rail"), ("Edge", "Road"),
            ("Rail", "Empty"), ("Rail", "Rail"),
            ("Road", "Empty"), ("Road", "Road")
        ]
        is_connected = (conn1, conn2) in [("Road", "Road"), ("Rail", "Rail")]
        return [((conn1, conn2) in allowed_connections), is_connected]

    def is_connection_allowed(self, i, j, game_board, top_face):
        left_conn = self.get_left_neighbor_conn(i, j, game_board)
        top_conn = self.get_top_neighbor_conn(i, j, game_board)
        right_conn = self.get_right_neighbor_conn(i, j, game_board)
        bottom_conn = self.get_bottom_neighbor_conn(i, j, game_board)

        left_match, left_connected = self.match_connection(left_conn, top_face.left_conn)
        right_match, right_connected = self.match_connection(right_conn, top_face.right_conn)
        top_match, top_connected = self.match_connection(top_conn, top_face.top_conn)
        bottom_match, bottom_connected = self.match_connection(bottom_conn, top_face.bottom_conn)

        print(i,j)
        print(left_conn, top_face.left_conn)
        print(top_conn, top_face.top_conn)
        print(right_conn, top_face.right_conn)
        print(bottom_conn, top_face.bottom_conn)
        print(left_match)
        print(top_match)
        print(right_match)
        print(bottom_match)

        #The logic is as follows - There should be atleast one connection (rest can be not connected)
        return  (left_connected or right_connected or top_connected or bottom_connected) \
                and left_match and top_match and right_match and bottom_match

    def set_connections(self, top_face):
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = top_face.left_conn, top_face.top_conn, top_face.right_conn, top_face.bottom_conn

class GameBoard:
    def __init__(self, origin_x, origin_y, side_length):
        self.origin = (origin_x, origin_y)
        self.side_length = side_length
        self.draw_board = pygame.Rect(origin_x, origin_y, self.side_length, self.side_length)
        self.notice_board = pygame.Rect(540, 280, 280, 60)

        self.Buttons = pygame.sprite.Group()
        self.button_types = {"Roll":[560, 611, 67.45, 30],
                             "Undo":[660, 611, 67.5, 30],
                             "Restart":[740, 611, 67, 30],
                             "use1":[600, 381, 60, 60],
                             "use2":[700, 381, 60, 60],
                             "use3":[601, 461, 60, 60],
                             "use4":[701, 461, 60, 60],
                             "rotate":[626, 555, 50, 30],
                             "mirror":[686, 555, 50, 30],
                             "rotate_special":[520,156,50,20],
                             "score":[660,240,64,30]
        }

        for button_type, button in self.button_types.items():
            self.Buttons.add(Button(button, button_type))

        self.round_number = 0
        self.score = 0

        self.grid_squares = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(7):
                self.grid_squares[i].append(GridSquare(j, i, self))
        self.grid_squares = np.array(self.grid_squares)

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

        self.grid_squares = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(7):
                self.grid_squares[i].append(GridSquare(i, j, self))
        self.grid_squares = np.array(self.grid_squares)

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
        for grid_square in self.grid_squares.flatten():
            if grid_square.square.collidepoint(x,y):
                return grid_square

        return None


    def get_button_type(self, x, y):
        for button in self.Buttons:
            if button.is_pressed(x,y):
                return button.get_name()

        for grid_square in self.grid_squares.flatten():
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







