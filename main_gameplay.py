import pygame
import os

from loads.load_images import *
from loads.load_fonts import *
from board import GameBoard

pygame.init()

FPS = 60 #Screen's Update Frequency


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad Ink")

GB = GameBoard(60,260,420)


def update_board(square_on_board, board_dice):
	WIN.blit(BOARD, (0, 0))
	if square_on_board is not None:
		WIN.blit(SQUARE_SELECT, square_on_board.origin)

	for die in board_dice.get_dice():
		top_face = die.get_top_face()
		if top_face is not None:
			WIN.blit(top_face.get_image(), die.get_origin())
		if die.get_use() == True:
			x,y,_,_ = GB.button_types["use{}".format(die.dice_num)]
			WIN.blit(USE_SELECTED, (x,y))

	if GB.temp_die is not None:
		x, y, _, _ = GB.button_types["use{}".format(GB.temp_die.dice_num)]
		WIN.blit(USE_CAN_SELECT, (x, y))

	for grid_square in GB.grid_squares:
		if grid_square.top_face is not None:
			WIN.blit(grid_square.top_face.get_image(), grid_square.origin)

	for i in range(len(GB.stack)):
		elem_die, selected_square = GB.stack[i]
		WIN.blit(elem_die.get_top_face().get_image(), selected_square.origin)

	pygame.display.update()


def do_action_on_button_press(button_type, x, y):
	if GB.use_pressed == True:
		if button_type == "grid_square":
			selected_square = GB.get_square_under_mouse(*pygame.mouse.get_pos())
			if GB.temp_die is not None:
				if GB.temp_die.get_use() is False:
					GB.temp_die.set_use(True)
					GB.stack.append((GB.temp_die, selected_square))
				else:
					print("Die already used")

		GB.use_pressed = False
		GB.temp_die = None

	else:
		if button_type == "Roll":
			if (GB.round_number == 0) or (len(GB.stack) == 4):
				while(len(GB.stack) > 0):
					temp_die, selected_square = GB.stack.pop()
					selected_square.set_top_face(temp_die.get_top_face())
					selected_square.make_top_face_permanent()
				GB.stack.clear()
				GB.dice.roll()
				GB.round_number += 1
				for grid_square in GB.grid_squares:
					if (grid_square.top_face is not None) and (grid_square.is_permanent == False):
						grid_square.is_permanent = True

			elif button_type == "Restart":
				pass

			else:
				print("Some Dice are unused, use before Rolling")

		if GB.round_number >= 1:
			if button_type == "Undo":
				if len(GB.stack) > 0:
					die, _ = GB.stack.pop()
					die.set_use(False) #Can be used again because of the undo action
				for grid_square in GB.grid_squares:
					if (grid_square.top_face is not None) and (grid_square.is_permanent == False):
						grid_square.top_face = None

			elif "use" in button_type:
				GB.use_pressed = True
				die_num = int(button_type[-1])
				GB.temp_die = GB.dice.get_dice()[die_num - 1]

			elif "rotate" in button_type:
				die_num = int(button_type[-1])
				GB.dice.get_dice()[die_num - 1].rotate_face()

			elif "mirror" in button_type:
				die_num = int(button_type[-1])
				GB.dice.get_dice()[die_num - 1].mirror_face()

			else:
				GB.use_pressed = False
				GB.temp_die = None



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
					x,y = pygame.mouse.get_pos()
					button_type = GB.get_button_type(x,y)
					if button_type is not None:
						do_action_on_button_press(button_type, x, y)
					else:
						GB.use_pressed = False
						GB.temp_die = None


		print(GB.temp_die)
		print(GB.use_pressed)
		square_on_board = GB.get_square_under_mouse(*pygame.mouse.get_pos())
		update_board(square_on_board, GB.dice)


if __name__ == "__main__":
	main()