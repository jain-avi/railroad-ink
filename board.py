import pygame
from loads.load_images import *
from loads.load_fonts import *
from dice import Dice, SpecialConnection
from buttons import Button
from collections import deque
from loads.load_images import SP_JUNC_1, SP_JUNC_2, SP_JUNC_3, SP_JUNC_4, SP_JUNC_5, SP_JUNC_6
import numpy as np
from graph import BoardGraph
import time

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

    def get_board_indices(self, game_board):
        return (self.origin[1] - game_board.origin[1])//60, (self.origin[0] - game_board.origin[0])//60

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

        # print(i,j)
        # print(left_conn, top_face.left_conn)
        # print(top_conn, top_face.top_conn)
        # print(right_conn, top_face.right_conn)
        # print(bottom_conn, top_face.bottom_conn)
        # print(left_match)
        # print(top_match)
        # print(right_match)
        # print(bottom_match)

        #The logic is as follows - There should be atleast one connection (rest can be not connected)
        return  (left_connected or right_connected or top_connected or bottom_connected) \
                and left_match and top_match and right_match and bottom_match

    def set_connections(self, top_face):
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = top_face.left_conn, top_face.top_conn, top_face.right_conn, top_face.bottom_conn

    def process_after_click(self, GB, x, y):
        if (GB.grid_square_in_stack(self) is False) and (self.is_permanent is False):
            if GB.special_face_selected is not None:
                i, j = self.get_position(x, y, GB)
                if self.is_connection_allowed(i, j, GB, GB.special_face_selected) == True:
                    self.set_connections(GB.special_face_selected)
                    # print(self.get_connections())

                    GB.special_stack.append((GB.special_face_selected, self))
                    GB.last_actions.append("Special_Face_Added")
                else:
                    GB.temp_text = "Illegal Connection"
                    GB.start_time_for_temp_text = time.time()
                GB.special_face_selected = None

            elif GB.temp_die is not None:

                i, j = self.get_position(x, y, GB)
                if self.is_connection_allowed(i, j, GB, GB.temp_die.get_top_face()) == True:
                    GB.temp_die.set_use(True)
                    self.set_connections(GB.temp_die.get_top_face())
                    # print(self.get_connections())

                    GB.stack.append((GB.temp_die, self))
                    GB.last_actions.append("Die_Face_Added")
                else:
                    GB.temp_text = "Illegal Connection"
                    GB.start_time_for_temp_text = time.time()
                GB.use_pressed = False
                GB.temp_die = None
        elif (self.is_permanent is True):
            GB.temp_text = "Square is already used in previous rounds"
            GB.start_time_for_temp_text = time.time()
        else:
            GB.temp_text = "Square already used this round"
            GB.start_time_for_temp_text = time.time()


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

        self.graph = BoardGraph()

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

        self.graph = BoardGraph()

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


    def undo_last_action(self):
        if len(self.last_actions) > 0:
            last_action = self.last_actions.pop()
            if last_action == "Die_Face_Added":
                if len(self.stack) > 0:
                    die, selected_square = self.stack.pop()
                    die.set_use(False)  # Can be used again because of the undo action
                    selected_square.set_connections_to_None()

            elif last_action == "Special_Face_Added":
                if len(self.special_stack) > 0:
                    special_face, selected_square = self.special_stack.pop()
                    selected_square.set_connections_to_None()

    def set_temp_die(self, button_type):
        die_num = int(button_type[-1])
        self.temp_die = self.dice.get_dice()[die_num - 1]
        if self.temp_die.get_use() is True:
            self.temp_text = "Die already used this round"
            self.start_time_for_temp_text = time.time()
            self.temp_die = None
        else:
            self.use_pressed = True


    def set_special_face_temp(self, x, y):
        if len(self.special_faces_used) < 3:
            if len(self.special_stack) == 0:
                for special_face in self.special_connections:
                    if special_face.is_selected(x, y):
                        if special_face.get_use() is not True:
                            self.special_face_selected = special_face
                        else:
                            self.temp_text = "Special Connection is already used previously"
                            self.start_time_for_temp_text = time.time()
            else:
                self.temp_text = "Special Connection is already used this round"
                self.start_time_for_temp_text = time.time()
        else:
            self.temp_text = "Max 3 Special Connections can be used"
            self.start_time_for_temp_text = time.time()


    def make_special_connection_final(self):
        if len(self.special_stack) != 0:
            special_face, selected_square = self.special_stack.pop()
            special_face.is_used = True
            selected_square.set_top_face(special_face)
            selected_square.used_in_round = self.round_number
            self.special_stack.clear()
            self.special_faces_used.append(special_face)


    def make_die_faces_final(self):
        if (self.round_number == 0) or (len(self.stack) == 4):
            while (len(self.stack) > 0):
                temp_die, selected_square = self.stack.pop()
                selected_square.set_top_face(temp_die.get_top_face())
                selected_square.make_top_face_permanent()
                selected_square.used_in_round = self.round_number
            self.stack.clear()
            self.dice.roll()
            self.round_number += 1
            for grid_square in self.grid_squares.flatten():
                if (grid_square.top_face is not None) and (grid_square.is_permanent == False):
                    grid_square.is_permanent = True

            self.last_actions.clear()

        else:
            self.temp_text = "Some dice are unused in this round, use them first"
            self.start_time_for_temp_text = time.time()


    def update_display_for_grid_squares(self, WIN, square_on_board):
        if square_on_board is not None:
            WIN.blit(SQUARE_SELECT, square_on_board.origin)

        for grid_square in self.grid_squares.flatten():
            if grid_square.top_face is not None:
                WIN.blit(grid_square.top_face.get_image(), grid_square.origin)
            if grid_square.used_in_round is not None:
                round_number_text = NUMBER_FONT.render("{}".format(grid_square.used_in_round), 1, (0, 0, 0))
                x, y = grid_square.origin
                WIN.blit(round_number_text, (x + 46, y + 2))


    def update_display_for_special_connections(self, WIN):
        for special_face in self.special_connections:
            WIN.blit(special_face.get_image(), (special_face.face.x, special_face.face.y))
            if special_face.get_use() == True:
                WIN.blit(SPECIAL_SELECTED, (special_face.face.x, special_face.face.y))

        for special_face, selected_square in self.special_stack:
            WIN.blit(special_face.get_image(), selected_square.origin)
            WIN.blit(SPECIAL_SELECTED, (special_face.face.x, special_face.face.y))

        if self.special_face_selected is not None:
            x, y = self.special_face_selected.face.x, self.special_face_selected.face.y
            WIN.blit(SPECIAL_CAN_SELECT, (x, y))


    def update_display_for_die_faces(self, WIN, board_dice):
        for die in board_dice.get_dice():
            top_face = die.get_top_face()
            if top_face is not None:
                WIN.blit(top_face.get_image(), die.get_origin())
            if die.get_use() == True:
                x, y, _, _ = self.button_types["use{}".format(die.dice_num)]
                WIN.blit(USE_SELECTED, (x, y))

        if self.temp_die is not None:
            x, y, _, _ = self.button_types["use{}".format(self.temp_die.dice_num)]
            WIN.blit(USE_CAN_SELECT, (x, y))

        for i in range(len(self.stack)):
            elem_die, selected_square = self.stack[i]
            WIN.blit(elem_die.get_top_face().get_image(), selected_square.origin)


    def update_notice_board(self, WIN):
        round_text = ROUND_FONT.render("ROUND {}".format(self.round_number), 1, (0, 0, 0))
        WIN.blit(round_text, (self.notice_board.centerx - round_text.get_width() / 2, self.notice_board.y))
        if self.round_number == 0:
            self.temp_text = "Press Roll Dice to start the game"
            self.start_time_for_temp_text = time.time()
        rendered_temp_text = TEMP_FONT.render(self.temp_text, 1, (0, 0, 0))
        WIN.blit(rendered_temp_text, (self.notice_board.x + 10, self.notice_board.y + 30))





