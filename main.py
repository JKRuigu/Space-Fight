import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

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


pygame.init()

# create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
maxX,minX = 710,-10

# screen title
pygame.display.set_caption("Space Fight")

# Player
playerX,playerY = 370,480
player_change = 0
speed = 1

def player(x,y):
	screen.blit(YELLOW_SPACE_SHIP,(x,y))

# Player
enemyX,enemyY = random.randint(-10,710),50
enemy_changeX,enemy_changeY,speed = 1,40,1

def enemy(x,y):
	screen.blit(RED_SPACE_SHIP,(x,y))


# game loop
running = True
while running:
	screen.fill((0,0,0))		
	screen.blit(BG,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:	
			if event.key == pygame.K_LEFT:
				player_change = -speed
			if event.key == pygame.K_RIGHT:
				player_change = speed
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or	event.key == pygame.K_RIGHT:
				player_change = 0

	playerX += player_change
	if playerX <= minX:
		playerX = minX
	elif playerX >= maxX:
		playerX = maxX

	if enemyX <= minX:
		enemy_changeX = speed
		enemyY +=enemy_changeY
	elif enemyX >= 740:
		enemy_changeX =-speed
		enemyY +=enemy_changeY
	enemyX +=enemy_changeX # this comes after the if statement to have a smooth downwards transition

	player(playerX,playerY)
	enemy(enemyX,enemyY)		
	pygame.display.update()