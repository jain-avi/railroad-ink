import pygame.sprite

from loads.load_images import *
from numpy import random as npr
import random

class DieFace():
    def __init__(self, img):
        self.img = img
        self.rotation_angle = 0
        self.is_mirrored = False
        self.img_conn_mapping = {
            STRAIGHT_HIGHWAY:["Road", "Empty", "Road", "Empty"],
            STRAIGHT_RAILWAY: ["Empty", "Rail", "Empty", "Rail"],
            CURVED_HIGHWAY: ["Empty", "Empty", "Road", "Road"],
            CURVED_RAILWAY: ["Empty", "Empty", "Rail", "Rail"],
            STRAIGHT_STATION: ["Empty", "Rail", "Empty", "Road"],
            CURVED_STATION: ["Empty", "Empty", "Rail", "Road"],
            T_HIGHWAY: ["Road", "Empty", "Road", "Road"],
            T_RAILWAY: ["Empty", "Rail", "Rail", "Rail"],
            STRAIGHT_OVERPASS: ["Road", "Rail", "Road", "Rail"],
        }

        # Changes made are now for the graph to be created
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = self.img_conn_mapping[img]

    def rotate(self):
        self.rotation_angle -= 90
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = self.bottom_conn, self.left_conn, self.top_conn, self.right_conn

    def mirror(self):
        self.is_mirrored = not self.is_mirrored
        self.left_conn, self.right_conn = self.right_conn, self.left_conn

    def get_image(self):
        die_face_img = self.img
        if self.is_mirrored == True:
            die_face_img = pygame.transform.flip(die_face_img, flip_x=True, flip_y=False)
        die_face_img = pygame.transform.rotate(die_face_img, self.rotation_angle)
        return die_face_img


class SpecialConnection(pygame.sprite.Sprite):
    def __init__(self, img, face_params):
        super(SpecialConnection, self).__init__()
        self.img = img
        self.rotation_angle = 0
        self.is_used = False
        self.face = pygame.Rect(*face_params)

        self.img_conn_mapping = {
            SP_JUNC_1: ["Rail", "Road", "Road", "Road"],
            SP_JUNC_2: ["Rail", "Rail", "Rail", "Road"],
            SP_JUNC_3: ["Road", "Road", "Road", "Road"],
            SP_JUNC_4: ["Rail", "Rail", "Rail", "Rail"],
            SP_JUNC_5: ["Road", "Rail", "Rail", "Road"],
            SP_JUNC_6: ["Road", "Rail", "Road", "Rail"],
        }

        # Changes made are now for the graph to be created
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = self.img_conn_mapping[img]

    def rotate(self):
        self.rotation_angle -= 90
        self.left_conn, self.top_conn, self.right_conn, self.bottom_conn = self.bottom_conn, self.left_conn, self.top_conn, self.right_conn

    def get_image(self):
        die_face_img = pygame.transform.rotate(self.img, self.rotation_angle)
        return die_face_img

    def is_selected(self, x, y):
        return self.face.collidepoint(x, y)

    def get_use(self):
        return self.is_used

    def set_use(self, bool_var):
        self.is_used = bool_var


class Die(pygame.sprite.Sprite):
    def __init__(self, dice_num, type_dice):
        super(Die, self).__init__()
        if type_dice == 1:
            self.faces = [STRAIGHT_HIGHWAY, STRAIGHT_RAILWAY, CURVED_HIGHWAY, CURVED_RAILWAY, T_HIGHWAY, T_RAILWAY]
        else:
            self.faces = [STRAIGHT_OVERPASS, STRAIGHT_STATION, CURVED_STATION, STRAIGHT_OVERPASS, STRAIGHT_STATION, CURVED_STATION]
        self.current_top_face = None
        self.dice_num = dice_num
        self.is_used = False

    def roll(self, val):
        self.current_top_face = DieFace(self.faces[val])

    def rotate_face(self):
        if self.current_top_face is not None:
            self.current_top_face.rotate()
        else:
            print("No Dice Rolled, first roll the dice to get the connection")

    def mirror_face(self):
        if self.current_top_face is not None:
            self.current_top_face.mirror()
        else:
            print("No Dice Rolled, first roll the dice to get the connection")

    def get_top_face(self):
        return self.current_top_face

    def get_origin(self):
        if self.dice_num == 1:
            return (600, 381)
        elif self.dice_num == 2:
            return (700, 381)
        elif self.dice_num == 3:
            return (601, 461)
        else:
            return (701, 461)

    def get_use(self):
        return self.is_used

    def set_use(self, bool_val):
        self.is_used = bool_val

class Dice():
    def __init__(self, num_dice = 4,dice_types = [1,1,1,2]):
        self.dice_group = []
        self.num_dice = 4
        self.dice_types = dice_types

    def roll(self):
        self.dice_group = []
        for die_num, die_type in zip(list(range(1, self.num_dice+1)), self.dice_types):
            temp_die = Die(die_num, die_type)
            self.dice_group.append(temp_die)

        random_dice = npr.randint(6, size=self.num_dice)
        for i in range(len(self.dice_group)):
            random.shuffle(self.dice_group[i].faces)
            self.dice_group[i].roll(random_dice[i])

    def get_dice(self):
        return self.dice_group


