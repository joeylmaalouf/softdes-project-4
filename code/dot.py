import pygame
import sys
import math
import time
from utils import *
from operator import add

def main(argv):
	pygame.init()
	gameRunning = True

	loseFont = pygame.font.Font(None, 80)
	ballCountFont = pygame.font.Font(None, 900)
	scoreFont = pygame.font.Font(None, 22)

	width = 1500
	height = 800
	size = width, height
	displayObject = DisplayObject(1500, 800)
	screen = pygame.display.set_mode(size)
	background_color = 0, 0, 0

	player = Player(pos = Vector(width/2, height/2), speed = 10, suck_radius = 60, pickup_dist = 10)

	# Initialize game variables
	enemies = []
	enemies.append(Enemy(pos=Vector(100, 100)))
	balls = []
	balls_to_be_added = []
	ammo = []
	score = 0

	for x in range(0, width, 15):
		for y in range(0, height, 15):
			balls.append(Ball(pos = Vector(x, y), vel = Vector(0, 0)))

	while gameRunning:
		screen.fill(background_color)
		#Draw ball count first so it appears behind everything
		ballCount_textSurface = ballCountFont.render(str(len(ammo)), True, (7,7,7)) #Print 'You lose' screen
		ballCount_textRect = ballCount_textSurface.get_rect()
		ballCount_textRect.center = ((width/2),(height/2))
		screen.blit(ballCount_textSurface, ballCount_textRect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		#Process movement
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_ESCAPE]:
			sys.exit()
		movement_dir = (Vector(-int(pressed_keys[pygame.K_a]), 0) + Vector(int(pressed_keys[pygame.K_d]), 0) + Vector(0, -int(pressed_keys[pygame.K_w])) + Vector(0, int(pressed_keys[pygame.K_s]))).norm()
		player.pos = player.pos + (movement_dir * player.speed)	
		if player.pos.x < 0:
			player.pos.x = 0
		elif player.pos.x > width:
			player.pos.x = width
		if player.pos.y < 0:
			player.pos.y = 0
		elif player.pos.y > height:
			player.pos.y = height

		#Process aiming
		mouse_pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		aim_dir = (mouse_pos - player.pos).norm()

		mouse_clicks = pygame.mouse.get_pressed()
		if mouse_clicks[0]: #LMB PRESSED
			player.sucking = True
		else:
			player.sucking = False
			if len(ammo) > 10:
				for ball in ammo[0:10]:
					ball.held = False
					ball.pos = player.pos * 1.0
					ball.fire(aim_dir)
				ammo = ammo[10:]


		for ball in balls:
			if ball.held:
				pass #Dont care about held balls
			else:
				if player.sucking:
					suck_direction = player.pos - ball.pos
					dist = suck_direction.getMag()
					if dist <= player.suck_radius and player.sucking:
						if dist <= player.pickup_dist:
							ball.held = True
							ammo.append(ball)
						else:
							ball.vel = suck_direction * .7
				if not ball.vel.getMag() == 0: #only do the movement calc for balls that are not standing still
					ball.move(displayObject)
					if ball.vel.getMag() > 50: #if ball velocity is greater than the kill threshold
						k = 0
						while k < len(enemies):
							if (enemies[k].pos - ball.pos).getMag() < 5:
								balls_to_be_added.extend(enemies[k].kill())
								score += 1 #Add one to the kill count
								enemies.append(Enemy(pos = Vector(random.randint(100, 1400), random.randint(100, 700))))
								if random.randint(1, 100)>90: #10% chance of spawning in another enemy!
									enemies.append(Enemy(pos = Vector(random.randint(100, 1400), random.randint(100, 700))))
								del(enemies[k])
							else:
								k += 1
				ball.draw(screen)
				balls.extend(balls_to_be_added)
				balls_to_be_added = []

		for enemy in enemies:
			direction = (player.pos - enemy.pos)
			if direction.getMag() <= player.killDist:
				gameRunning = False
			enemy.move(direction.norm())
			enemy.draw(screen)
		player.draw(screen)
		pygame.display.flip()

	# Draw Game Over screen
	s = pygame.Surface((width,height), pygame.SRCALPHA)
	s.fill((0,0,0,180)) #Draw black transparent rectangle over screen
	screen.blit(s, (0,0))

	lose_textSurface = loseFont.render("You Lose", True, (255,255,255)) #Print 'You lose' screen
	lose_textRect = lose_textSurface.get_rect()
	lose_textRect.center = ((width/2),(height/2))
	screen.blit(lose_textSurface, lose_textRect)

	score_textSurface = scoreFont.render("You out-lived " + str(score) + " evil communist circles", True, (255,255,255)) #Print score
	score_textRect = score_textSurface.get_rect()
	score_textRect.center = ((width/2),(height/2) + lose_textRect.height)
	screen.blit(score_textSurface, score_textRect)

	pygame.display.flip()
	time.sleep(.5)
	while not any(x > 0 for x in pygame.key.get_pressed()):
		pygame.event.get()
		time.sleep(.001)



if __name__ == "__main__":
	main(sys.argv)
