import pygame
import os
import time
import random
import math
import neat

pygame.font.init()

WIDTH, HEIGHT = 800, 600
font = pygame.font.Font('freesansbold.ttf',40)
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
	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Enemy():
	speed = 5
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.change = 5
		self.img = RED_SPACE_SHIP

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))

	def move(self):
		self.y += self.speed

	def collide(self, player, win):
		bird_mask = player.get_mask()
		bottom_mask = pygame.mask.from_surface(self.img)
		bottom_offset = (self.x - player.x, self.y - round(player.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)

		if b_point:
			return True

		return False

def draw_win(win,player,enemies,score):
	win.blit(BG, (0,0))
	score_label = font.render("Score: " + str(score),1,(255,255,255))
	win.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))
	player.draw(win)
	for enemy in enemies:
		enemy.draw(win)
	pygame.display.update()

def main():
	player = Player(370,480)
	enemies = [Enemy(random.randint(-10,710),random.randint(0,50)),Enemy(random.randint(-10,710),random.randint(0,50)),Enemy(random.randint(-10,710),random.randint(0,50))]
	run = True
	win = pygame.display.set_mode((WIDTH,HEIGHT))
	clock = pygame.time.Clock()
	score = 0
	while run:
		# clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		add_enemy = False
		rem = []
		for enemy in enemies:
			if enemy.collide(player,win):
				pass
			if enemy.y >= 500:
				print("collide")
				score+=1
				rem.append(enemy)
				add_enemy = True
			enemy.move()
		if add_enemy:
			enemies.append(Enemy(random.randint(-10,710),random.randint(0,50)))	
		for r in rem:
			enemies.remove(r)		
		draw_win(win,player,enemies,score)

main()
# def run(config_file):
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_file)

#     p = neat.Population(config)

#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)

#     winner = p.run(main_menu, 50)

#     # # show final stats
#     # print('\nBest genome:\n{!s}'.format(winner))


# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config-feedforward.txt')
#     run(config_path)
