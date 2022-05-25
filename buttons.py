import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, rect_params, button_name):
        super(Button, self).__init__()
        self.button = pygame.Rect(*rect_params)
        self.name = button_name

    def is_pressed(self, x, y):
        return self.button.collidepoint(x,y)

    def get_name(self):
        return self.name

