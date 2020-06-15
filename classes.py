import pygame
import os
import time
import random
import math
import neat

pygame.font.init()

WIDTH, HEIGHT = 800, 600
font = pygame.font.Font('freesansbold.ttf',32)
over_font = pygame.font.Font('freesansbold.ttf',90)
score = 0

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


# create win
pygame.init()

class Player():
	player_speed = 5
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.change = 5
		self.img = YELLOW_SPACE_SHIP

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))

	def move(self,ch):
		self.x += (self.change*ch)
		if self.x <= -10:
			self.x = -10
		elif self.x >= 710:
			self.x = 710

def draw_win(win,player):
	win.blit(BG, (0,0))
	player.draw(win)
	pygame.display.update()

def main():
	player = Player(370,480)
	run = True
	win = pygame.display.set_mode((WIDTH,HEIGHT))
	clock = pygame.time.Clock()

	while run:
		# clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				if event.key == pygame.K_LEFT:
					player.move(-1)
				if event.key == pygame.K_RIGHT:
					player.move(1)
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or	event.key == pygame.K_RIGHT:
					player.move(0)

		draw_win(win,player)
main()