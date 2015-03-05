import pygame
import sys
import math
import time
from utils import *
from operator import add

pygame.init()
myfont = pygame.font.Font(None, 30)
width = 1500
height = 800
size = width, height
displayObject = DisplayObject(1500, 800)
screen = pygame.display.set_mode(size)
background_color = 0, 0, 0

player = Player(pos = Vector(width/2, height/2), speed = 10, suck_radius = 60, pickup_dist = 10)

enemies = []
enemies.append(Enemy(pos=Vector(523, 123)))
balls = []
balls_to_be_added = []
ammo = []

for x in range(0, width, 20):
	for y in range(0, height, 20):
		balls.append(Ball(pos = Vector(x, y), vel = Vector(0, 0)))

while 1:
	screen.fill(background_color)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	#Process movement
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[pygame.K_ESCAPE]:
		sys.exit()
	movement_dir = (Vector(-int(pressed_keys[pygame.K_a]), 0) + Vector(int(pressed_keys[pygame.K_d]), 0) + Vector(0, -int(pressed_keys[pygame.K_w])) + Vector(0, int(pressed_keys[pygame.K_s]))).norm()
	player.pos = player.pos + (movement_dir * player.speed)	

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
							enemies.append(Enemy(pos = Vector(random.randint(100, 1400), random.randint(100, 700))))
							del(enemies[k])
						else:
							k += 1
			ball.draw(screen)
			balls.extend(balls_to_be_added)
			balls_to_be_added = []

	for enemy in enemies:
		enemy.move((player.pos - enemy.pos).norm())
		enemy.draw(screen)
	player.draw(screen)
	pygame.display.flip()