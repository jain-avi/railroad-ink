import pygame

class GridSquare(pygame.sprite.Sprite):
    def __init__(self, i, j, game_board):
        super(GridSquare, self).__init__()
        self.origin = (game_board.origin[0] + i*60, game_board.origin[1] + j*60)
        self.square = pygame.Rect(self.origin[0], self.origin[1], game_board.side_length//7, game_board.side_length//7)

class GameBoard:
    def __init__(self, origin_x, origin_y, side_length):
        self.origin = (origin_x, origin_y)
        self.side_length = side_length
        self.draw_board = pygame.Rect(origin_x, origin_y, self.side_length, self.side_length)

        self.roll_dice_box = pygame.Rect(572, 688, 67.45, 30)
        self.undo_box = pygame.Rect(673.5, 687.9, 67.5, 30)
        self.restart_game_box = pygame.Rect(780, 687.5, 67, 30)

        self.undo1 = pygame.Rect(640,375,50,30)
        self.undo2 = pygame.Rect(640, 455, 50, 30)
        self.undo3 = pygame.Rect(640, 535, 50, 30)
        self.undo4 = pygame.Rect(640, 615, 50, 30)

        self.rotate1 = pygame.Rect(700,375,50,30)
        self.rotate2 = pygame.Rect(700, 455, 50, 30)
        self.rotate3 = pygame.Rect(700, 535, 50, 30)
        self.rotate4 = pygame.Rect(700, 615, 50, 30)

        self.mirror1 = pygame.Rect(760,375,50,30)
        self.mirror2 = pygame.Rect(760, 455, 50, 30)
        self.mirror3 = pygame.Rect(760, 535, 50, 30)
        self.mirror4 = pygame.Rect(760, 615, 50, 30)

        self.round_number = 1
        self.score = 0

        self.grid_squares = pygame.sprite.Group()
        for i in range(7):
            for j in range(7):
                self.grid_squares.add(GridSquare(i, j, self))

    def get_square_under_mouse(self, x, y):
        for grid_square in self.grid_squares:
            if grid_square.square.collidepoint(x,y):
                return grid_square

        return None






