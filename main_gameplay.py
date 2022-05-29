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
	if square_on_board is not None:
		WIN.blit(SQUARE_SELECT, square_on_board.origin)

	for special_face in GB.special_connections:
		WIN.blit(special_face.get_image(), (special_face.face.x, special_face.face.y))
		if special_face.get_use() == True:
			WIN.blit(SPECIAL_SELECTED, (special_face.face.x, special_face.face.y))

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

	for grid_square in GB.grid_squares.flatten():
		if grid_square.top_face is not None:
			WIN.blit(grid_square.top_face.get_image(), grid_square.origin)
		if grid_square.used_in_round is not None:
			round_number_text = NUMBER_FONT.render("{}".format(grid_square.used_in_round), 1, (0, 0, 0))
			x,y = grid_square.origin
			WIN.blit(round_number_text, (x+46,y+2))

	for i in range(len(GB.stack)):
		elem_die, selected_square = GB.stack[i]
		WIN.blit(elem_die.get_top_face().get_image(), selected_square.origin)

	for special_face, selected_square in GB.special_stack:
		WIN.blit(special_face.get_image(), selected_square.origin)
		WIN.blit(SPECIAL_SELECTED, (special_face.face.x, special_face.face.y))

	if GB.special_face_selected is not None:
		x,y = GB.special_face_selected.face.x, GB.special_face_selected.face.y
		WIN.blit(SPECIAL_CAN_SELECT, (x,y))

	round_text = ROUND_FONT.render("ROUND {}".format(GB.round_number), 1, (0,0,0))
	WIN.blit(round_text, (GB.notice_board.centerx - round_text.get_width()/2, GB.notice_board.y))
	if GB.round_number == 0:
		GB.temp_text = "Press Roll Dice to start the game"
		GB.start_time_for_temp_text = time.time()
	rendered_temp_text = TEMP_FONT.render(GB.temp_text, 1, (0,0,0))
	WIN.blit(rendered_temp_text, (GB.notice_board.x + 10, GB.notice_board.y + 30))

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
			if (GB.grid_square_in_stack(selected_square) is False) and (selected_square.is_permanent is False):
				if GB.special_face_selected is not None:
					i,j = selected_square.get_position(x,y,GB)
					#print(selected_square.is_connection_allowed(i,j,GB, GB.special_face_selected))
					if selected_square.is_connection_allowed(i,j,GB, GB.special_face_selected) == True:
						selected_square.set_connections(GB.special_face_selected)
						print(selected_square.get_connections())

						GB.special_stack.append((GB.special_face_selected, selected_square))
						GB.last_actions.append("Special_Face_Added")
					else:
						GB.temp_text = "Illegal Connection"
						GB.start_time_for_temp_text = time.time()
					GB.special_face_selected = None

				elif GB.temp_die is not None:

					i, j = selected_square.get_position(x, y, GB)
					#print(selected_square.is_connection_allowed(i, j, GB, GB.temp_die.get_top_face()))
					if selected_square.is_connection_allowed(i, j, GB, GB.temp_die.get_top_face()) == True:
						GB.temp_die.set_use(True)
						selected_square.set_connections(GB.temp_die.get_top_face())
						print(selected_square.get_connections())

						GB.stack.append((GB.temp_die, selected_square))
						GB.last_actions.append("Die_Face_Added")
					else:
						GB.temp_text = "Illegal Connection"
						GB.start_time_for_temp_text = time.time()
					GB.use_pressed = False
					GB.temp_die = None
			elif (selected_square.is_permanent is True):
				GB.temp_text = "Square is already used in previous rounds"
				GB.start_time_for_temp_text = time.time()
			else:
				GB.temp_text = "Square already used this round"
				GB.start_time_for_temp_text = time.time()
		else:
			GB.use_pressed = False
			GB.temp_die = None
			GB.special_face_selected = None

	else:
		if button_type == "Roll":
			if GB.round_number <= 6:
				if len(GB.special_stack) != 0:
					special_face, selected_square = GB.special_stack.pop()
					special_face.is_used = True
					selected_square.set_top_face(special_face)
					selected_square.used_in_round = GB.round_number
					GB.special_stack.clear()
					GB.special_faces_used.append(special_face)

				if (GB.round_number == 0) or (len(GB.stack) == 4):
					while(len(GB.stack) > 0):
						temp_die, selected_square = GB.stack.pop()
						selected_square.set_top_face(temp_die.get_top_face())
						selected_square.make_top_face_permanent()
						selected_square.used_in_round = GB.round_number
					GB.stack.clear()
					GB.dice.roll()
					GB.round_number += 1
					for grid_square in GB.grid_squares.flatten():
						if (grid_square.top_face is not None) and (grid_square.is_permanent == False):
							grid_square.is_permanent = True

					GB.last_actions.clear()

				else:
					GB.temp_text = "Some dice are unused in this round, use them first"
					GB.start_time_for_temp_text = time.time()
			else:
				GB.temp_text = "Game Over, press Score to Finish"
				GB.start_time_for_temp_text = time.time()

		elif button_type == "Restart":
			GB.restart_game()

		if GB.round_number >= 1:
			if button_type == "Undo":
				if len(GB.last_actions)>0:
					last_action = GB.last_actions.pop()
					if last_action == "Die_Face_Added":
						if len(GB.stack) > 0:
							die, selected_square = GB.stack.pop()
							die.set_use(False) #Can be used again because of the undo action
							selected_square.set_connections_to_None()

					elif last_action == "Special_Face_Added":
						if len(GB.special_stack)>0:
							special_face, selected_square = GB.special_stack.pop()
							selected_square.set_connections_to_None()

			elif "use" in button_type:
				die_num = int(button_type[-1])
				GB.temp_die = GB.dice.get_dice()[die_num - 1]
				if GB.temp_die.get_use() is True:
					GB.temp_text = "Die already used this round"
					GB.start_time_for_temp_text = time.time()
					GB.temp_die = None
				else:
					GB.use_pressed = True

			# elif "rotate" in button_type:
			# 	die_num = int(button_type[-1])
			# 	if GB.dice.get_dice()[die_num - 1].get_use() == False:
			# 		GB.dice.get_dice()[die_num - 1].rotate_face()

			# elif "mirror" in button_type:
			# 	die_num = int(button_type[-1])
			# 	GB.dice.get_dice()[die_num - 1].mirror_face()

			elif button_type == "special_face":
				if len(GB.special_faces_used) < 3:
					if len(GB.special_stack) == 0:
						for special_face in GB.special_connections:
							if special_face.is_selected(x, y):
								if special_face.get_use() is not True:
									GB.special_face_selected = special_face
								else:
									GB.temp_text = "Special Connection is already used previously"
									GB.start_time_for_temp_text = time.time()
					else:
						GB.temp_text = "Special Connection is already used this round"
						GB.start_time_for_temp_text = time.time()
				else:
					GB.temp_text = "Max 3 Special Connections can be used"
					GB.start_time_for_temp_text = time.time()

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
						print("Button Pressed", button_type)
						do_action_on_button_press(button_type, x, y)
					else:
						GB.use_pressed = False
						GB.temp_die = None


		if GB.temp_text != "":
			if time.time() - GB.start_time_for_temp_text > 1.5:
				GB.temp_text = ""
				GB.start_time_for_temp_text = None

		square_on_board = GB.get_square_under_mouse(*pygame.mouse.get_pos())
		# if square_on_board is not None:
		# 	print(pygame.mouse.get_pos())
		# 	print(square_on_board.get_position(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], GB))
		update_board(square_on_board, GB.dice)


if __name__ == "__main__":
	main()