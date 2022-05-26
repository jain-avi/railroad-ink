import pygame
import os

WIDTH, HEIGHT = 840, 740
#Defining all the images to be loaded here
BOARD = pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'game_screen.png')), (WIDTH, HEIGHT))

#Load dice faces
STRAIGHT_HIGHWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','straight_highway.png')), (60, 60)
	)
STRAIGHT_RAILWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','straight_railway.png')), (60, 60)
	)
CURVED_HIGHWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','curved_highway.png')), (60, 60)
	)
CURVED_RAILWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','curved_railway.png')), (60, 60)
	)
T_HIGHWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','t_highway.png')), (60, 60)
	)
T_RAILWAY = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','t_railway.png')), (60, 60)
	)
STRAIGHT_STATION = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','straight_station.png')), (60, 60)
	)
CURVED_STATION = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','curved_station.png')), (60, 60)
	)
STRAIGHT_OVERPASS = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','straight_overpass.png')), (60, 60)
	)


#Load Special Junctions
SP_JUNC_1 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction1.png')), (60, 60)
	)
SP_JUNC_2 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction2.png')), (60, 60)
	)
SP_JUNC_3 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction3.png')), (60, 60)
	)
SP_JUNC_4 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction4.png')), (60, 60)
	)
SP_JUNC_5 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction5.png')), (60, 60)
	)
SP_JUNC_6 = pygame.transform.smoothscale(
	pygame.image.load(os.path.join('Images', 'board_graphics','special_junction6.png')), (60, 60)
	)


#Load the square selector
SQUARE_SELECT = pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'square_select.png')), (60, 60))
USE_SELECTED = pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'use_selected.png')), (50, 30))
USE_CAN_SELECT = pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'use_can_select.png')), (50, 30))