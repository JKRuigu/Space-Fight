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

def draw_win(win,players,enemies,score,gen):
	win.blit(BG, (0,0))
	score_label = font.render("Score: " + str(score),1,(255,255,255))
	win.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))

	gen = font.render("Gen: " + str(gen),1,(255,255,255))
	win.blit(gen, (10, 10))

	# alive
	players_pop = font.render("Alive: " + str(len(players)),1,(255,255,255))
	win.blit(players_pop, (10, 50))

	for player in players:
		player.draw(win)

	for enemy in enemies:
		enemy.draw(win)
	pygame.display.update()

def main(genomes,config):	
	global GEN
	GEN += 1
	enemies = [Enemy(random.randint(-10,710),random.randint(0,50)),Enemy(random.randint(-10,710),random.randint(0,50))]
	nets  =[] 
	ge = []
	players =[]
	clock = pygame.time.Clock()
	score = 0
	
	for g_id,g in genomes:
		g.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		players.append(Player(370,480))
		ge.append(g)

	win = pygame.display.set_mode((WIDTH,HEIGHT))
	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()

		for x,player in enumerate(players):
			ge[x].fitness +=0.1
			if player.x >= 0 or player.x <= 800:
				ge[x].fitness +=0.01
			elif player.x >= 0 or player.x >= 800:
				ge[x].fitness -=0.5
			if len(enemies) >0:
				for enemy in enemies:
					if abs(player.y - enemy.y) > 100:
						ge[x].fitness += 1.5
					output = nets[players.index(player)].activate((player.x, abs(player.y - enemy.y), abs(player.x - enemy.x)))
					num = int(output[0])
					if num == -1 or num == 1:
						player.move(num)
						ge[x].fitness +=.002

		add_enemy = False
		rem = []
		for enemy in enemies:
			enemy.move()
			for player in players:
				if enemy.collide(player,win):
					ge[players.index(player)].fitness -=5
					ge[players.index(player)].fitness -=1
					nets.pop(players.index(player))
					ge.pop(players.index(player))
					players.pop(players.index(player))

			if enemy.y >= 600:
				rem.append(enemy)

			if enemy.y >= 400:
					add_enemy = True

		if add_enemy and len(enemies) <3:
			score+=1
			for g in ge:
				g.fitness += 2
			enemies.append(Enemy(random.randint(-10,710),random.randint(0,50)))	
		add_enemy = False
			
		for r in rem:
			enemies.remove(r)

		for player in players:
			if player.x <= -5 or player.x>= 800:
				nets.pop(players.index(player))
				ge.pop(players.index(player))
				players.pop(players.index(player))
		if len(players) <= 0:
			for g in ge:
				players.append(Player(370,480))
		if score > 150 or len(players) <= 0:
			break
		draw_win(win,players,enemies,score,GEN)

def run(config_file):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(main, 50)

	with open('model_pickel','wb') as f:
		pickle.dump(winner,f)

	# show final stats
	print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)
