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


# create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
maxX,minX = 710,-10
# bullet_state
bullet_state = "ready"

def main():
	nets = []
	ge = []

	pygame.init()
	score = 0

	# screen title
	pygame.display.set_caption("Space Fight")
	textX =10
	textY =10

	# display score
	def show_score(x,y):
		text = font.render("Score: "+str(score),True,(255,255,255))
		screen.blit(text,(x,y))

	# display game over
	def game_over_text():
		over_text = font.render("GAME OVER",True,(255,255,255))
		screen.blit(over_text,(250,250))
	# Player
	playerX,playerY = 370,480
	player_change = 0
	player_speed = 5

	def player(x,y):
		screen.blit(YELLOW_SPACE_SHIP,(x,y))

	# Enemy
	enemyImg = []
	enemyX = []
	enemyY = []
	enemyX_change = []
	enemyY_change = []
	speed = []
	number_of_enemies = 5
	for i in range(number_of_enemies):
		enemyImg.append(RED_SPACE_SHIP)
		enemyX.append(random.randint(-10,710))
		enemyY.append(random.randint(50,150))
		enemyX_change.append(1)
		enemyY_change.append(40)
		speed.append(1)

	def enemy(x,y,i):
		screen.blit(enemyImg[i],(x,y))

	# BULLET
	bulletX = 0
	bulletY = 480
	bulletX_change = 0
	bulletY_change = 10
	bullet_state = "ready"

	def fire_bullet(x,y):
		bulletX = x
		screen.blit(RED_LASER,(x,y-50))

	# collition
	def isCollision(enemyX,enemyY,bulletX,bulletY):
		distance = math.sqrt((math.pow(enemyX - bulletX,2))+(math.pow(enemyY - bulletY,2)))

		if distance <27:
			return True
		else:
			return False

	# game loop
	running = True
	# def run():
	while running:
		screen.fill((0,0,0))		
		screen.blit(BG,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:	
				if event.key == pygame.K_LEFT:
					player_change = -player_speed
				if event.key == pygame.K_RIGHT:
					player_change = player_speed
				if event.key == pygame.K_SPACE:
					if bullet_state == "ready":
						bulletX = playerX
						bullet_state = "fire"
						fire_bullet(playerX,bulletY)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or	event.key == pygame.K_RIGHT:
					player_change = 0

		
		playerX += player_change

		# PLAYER MOVEMENT
		if playerX <= minX:
			playerX = minX
		elif playerX >= maxX:
			playerX = maxX

			# BULLET MOVEMENT
		if bullet_state == "fire":
			fire_bullet(bulletX,bulletY)
			bulletY -=bulletY_change
				
		if bulletY <= 0:
			print("ready")
			bulletY = playerY
			bullet_state = "ready"

		# ENEMIES MOVEMENT
		for i in range(number_of_enemies):
			if enemyY[i] > 440:
				for j in range(number_of_enemies):
					enemyY[j] = 2000
				game_over_text()
				break

			enemyX[i] +=enemyX_change[i] # this comes after the if statement to have a smooth downwards transition
			if enemyX[i] <= minX:
				enemyX_change[i] = 1
				enemyY[i] +=enemyY_change[i]
			elif enemyX[i] >= 740:
				enemyX_change[i] =-1
				enemyY[i] +=enemyY_change[i]


			collition = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
			if collition:
				bulletY =playerY
				print("collition")
				bullet_state = "ready"
				score +=1
				enemyX[i],enemyY[i] = random.randint(0,710),random.randint(50,150)
			
			# dis = math.sqrt((math.pow(enemyX[i] - bulletX[i],2))+(math.pow(enemyY[i] - bulletY[i],2)))

			enemy(enemyX[i],enemyY[i],i)		

		player(playerX,playerY)
		show_score(textX,textY)
		pygame.display.update()


def main_menu():
    title_font = pygame.font.Font('freesansbold.ttf',50)
    run = True
    while run:
        screen.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                pass
    pygame.quit()


# main_menu()
def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main_menu, 50)

    # # show final stats
    # print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # run(config_path)
    main_menu()
