import pygame
import os

from loads.load_images import *
from loads.load_fonts import *
from board import GameBoard

pygame.init()

FPS = 60 #Screen's Update Frequency


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad Ink")

game_board = GameBoard(60,260,420)


def update_board(square_on_board):
	WIN.blit(BOARD, (0, 0))
	if square_on_board is not None:
		WIN.blit(SQUARE_SELECT, square_on_board.origin)
	pygame.display.update()


def main():
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		square_on_board = game_board.get_square_under_mouse(*pygame.mouse.get_pos())
		update_board(square_on_board)


if __name__ == "__main__":
	main()