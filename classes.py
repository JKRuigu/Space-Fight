import pygame
import os
import time
import random
import math
import neat
import pickle

pygame.font.init()

WIDTH, HEIGHT = 800, 600
font = pygame.font.Font('freesansbold.ttf',40)
over_font = pygame.font.Font('freesansbold.ttf',90)
score = 0
GEN =0

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
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))

	def move(self,ch):
		self.x += (ch*self.player_speed)
		# if self.x <= -10:
		# 	self.x = -10
		# elif self.x >= 710:
		# 	self.x = 710
	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Enemy():
	speed = 5
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.change = 5
		self.img = RED_SPACE_SHIP
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))

	def move(self):
		self.y += self.speed

	def collide(self, player, win):
		bird_mask = player.get_mask()
		bottom_mask = pygame.mask.from_surface(self.img)
		bottom_offset = (self.x - player.x, self.y - round(player.y))
		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		# distance = math.sqrt((math.pow(player.x - self.x,2))+(math.pow(player.y - self.y,2)))
		if b_point:
			return True

		return False
	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x-20, self.y, self.img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.y += vel

	def off_screen(self, height):
		return not(self.y <= height and self.y >= 0)

	def collision(self, obj):
		return collide(self, obj)

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def draw_win(win,player,enemies,score,lasers):
	win.blit(BG, (0,0))
	score_label = font.render("Score: " + str(score),1,(255,255,255))
	win.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))

	player.draw(win)
	for laser in lasers:
		laser.draw(win)
		laser.move(-5)

	for enemy in enemies:
		enemy.draw(win)
	pygame.display.update()

def main():	
	enemies = [Enemy(370,100)]
	clock = pygame.time.Clock()
	score = 0
	player = Player(370,480)
	lasers = [Laser(370,400,YELLOW_LASER)]
	
	win = pygame.display.set_mode((WIDTH,HEIGHT))
	run = True
	while run:
		clock.tick(30)
		rem = []
		remLaser = []
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		for enemy in enemies:
			# enemy.move()
			for laser in lasers:
				if laser.collision(enemy) == True:
					rem.append(enemy)
					remLaser.append(laser)
					enemies.append(Enemy(370,50))

		for r in rem:
			enemies.remove(r)

		for r in remLaser:
			lasers.remove(r)


		draw_win(win,player,enemies,score,lasers)

main()
