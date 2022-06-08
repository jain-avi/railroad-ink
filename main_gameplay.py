from loads.load_images import *
from loads.load_fonts import *
from board import GameBoard
import time

pygame.init()

FPS = 60 #Screen's Update Frequency


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad Ink")

GB = GameBoard(60,260,420)


def update_board(square_on_board, board_dice):
	WIN.blit(BOARD, (0, 0))
	GB.update_display_for_grid_squares(WIN, square_on_board)
	GB.update_display_for_special_connections(WIN)
	GB.update_display_for_die_faces(WIN, board_dice)
	GB.update_notice_board(WIN)
	pygame.display.update()


def do_action_on_button_press(button_type, x, y):
	if GB.use_pressed == True or GB.special_face_selected is not None:
		if button_type == "rotate_special":
			GB.special_face_selected.rotate()
		elif button_type == "rotate":
			if GB.temp_die is not None:
				GB.temp_die.rotate_face()
		elif button_type == "mirror":
			if GB.temp_die is not None:
				GB.temp_die.mirror_face()
		elif button_type == "grid_square":
			selected_square = GB.get_square_under_mouse(*pygame.mouse.get_pos())
			selected_square.process_after_click(GB, x, y)
		else:
			GB.use_pressed = False
			GB.temp_die = None
			GB.special_face_selected = None

	else:
		if button_type == "Roll":
			if GB.round_number <= 6:
				GB.make_special_connection_final()
				GB.make_die_faces_final()
			else:
				GB.temp_text = "Game Over, press Score to Finish"
				GB.start_time_for_temp_text = time.time()

		elif button_type == "Restart":
			GB.restart_game()

		if GB.round_number >= 1:
			if button_type == "Undo":
				GB.undo_last_action()

			elif "use" in button_type:
				GB.set_temp_die(button_type)

			elif button_type == "special_face":
				GB.set_special_face_temp(x, y)

			elif button_type == "score":
				if GB.round_number == 7:
					pass
				else:
					GB.temp_text = "Game Finishes after Round 7"
					GB.start_time_for_temp_text = time.time()
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


		if GB.temp_text != "":
			if time.time() - GB.start_time_for_temp_text > 1.5:
				GB.temp_text = ""
				GB.start_time_for_temp_text = None

		square_on_board = GB.get_square_under_mouse(*pygame.mouse.get_pos())
		update_board(square_on_board, GB.dice)


if __name__ == "__main__":
	main()