from loads.load_images import *
import random

class DieFace():
    def __init__(self, img):
        self.img = img
        self.rotation_angle = 0
        self.is_mirrored = False

    def rotate(self):
        self.rotation_angle -= 90

    def mirror(self):
        self.is_mirrored = not self.is_mirrored

    def get_state(self):
        return self.rotation_angle, self.is_mirrored


class Die(pygame.sprite.Sprite):
    def __init__(self, dice_num, type_dice):
        super(Die, self).__init__()
        if type_dice == 1:
            self.faces = [STRAIGHT_HIGHWAY, STRAIGHT_RAILWAY, CURVED_HIGHWAY, CURVED_RAILWAY, T_HIGHWAY, T_RAILWAY]
        else:
            self.faces = [STRAIGHT_OVERPASS, STRAIGHT_OVERPASS, STRAIGHT_STATION, STRAIGHT_STATION, CURVED_STATION, CURVED_STATION]
        self.current_top_face = None
        self.dice_num = dice_num
        self.is_used = False

    def roll(self):
        random_face = random.randint(0,5)
        if self.current_top_face != None:
            print("The Round is not finished, use the connection shown in Dice {} first".format(self.dice_num))
        else:
            self.current_top_face = DieFace(self.faces[random_face])

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
            return (560, 360)
        elif self.dice_num == 2:
            return (560, 440)
        elif self.dice_num == 3:
            return (560, 520)
        else:
            return (560, 600)

class Dice():
    def __init__(self, num_dice = 4,dice_types = [1,1,1,2]):
        self.dice_group = []
        self.num_dice = 4
        self.dice_types = dice_types

    def roll(self):
        for die_num, die_type in zip(list(range(1, self.num_dice+1)), self.dice_types):
            temp_die = Die(die_num, die_type)
            self.dice_group.append(temp_die)

        for die in self.dice_group:
            die.roll()

    def get_dice(self):
        return self.dice_group

    def allNone(self):
        for die in self.dice_group:
            if die.current_top_face != None:
                return False
        return True


