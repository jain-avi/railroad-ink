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


def update_board(square_on_board, board_dice):
	WIN.blit(BOARD, (0, 0))
	if square_on_board is not None:
		WIN.blit(SQUARE_SELECT, square_on_board.origin)

	for die in board_dice.get_dice():
		top_face = die.get_top_face()
		if top_face is not None:
			die_face_img = pygame.transform.rotate(top_face.img, top_face.get_state()[0])
			if top_face.get_state()[1] == True:
				die_face_img = pygame.transform.flip(die_face_img,flip_x = True, flip_y=False)
			WIN.blit(die_face_img, die.get_origin())

	pygame.display.update()


def do_action_on_button_press(button_type):
	if button_type == "Roll":
		if game_board.dice.allNone():
			game_board.dice.roll()
	elif button_type == "Undo":
		pass
	elif button_type == "Restart":
		pass
	elif "use" in button_type:
		die_num = int(button_type[-1])
		pass
	elif "rotate" in button_type:
		die_num = int(button_type[-1])
		game_board.dice.get_dice()[die_num - 1].rotate_face()
	elif "mirror" in button_type:
		die_num = int(button_type[-1])
		game_board.dice.get_dice()[die_num - 1].mirror_face()
	else:
		pass

def main():
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_presses = pygame.mouse.get_pressed()
				if mouse_presses[0]:
					button_type = game_board.get_button_type(*pygame.mouse.get_pos())
					if button_type is not None:
						do_action_on_button_press(button_type)

		square_on_board = game_board.get_square_under_mouse(*pygame.mouse.get_pos())
		update_board(square_on_board, game_board.dice)


if __name__ == "__main__":
	main()