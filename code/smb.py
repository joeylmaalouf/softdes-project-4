""" Super Meat Boy
	in Python.
"""
from base import Camera, Entity
from levels import *

import cv2
from os.path import abspath, dirname
import pygame
import sys
import time


class MeatBoy(Entity):
	""" The Player object, representing
		the player's current state.
	"""

	def __init__(self, size = (32, 32), pos = (100, 100), speed = (0, 0)):
		super(MeatBoy, self).__init__(size, pos)
		self.vx = speed[0]
		self.vy = speed[1]
		self.grounded = False
		self.alive = True
		self.deaths = 0
		self.won = False


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution, camera, font):
		super(Game, self).__init__()
		self.resolution = resolution
		self.camera = camera
		self.font = font
		self.screen = pygame.display.set_mode(resolution)
		self.folderpath = dirname(abspath(__file__))
		pygame.display.set_caption("Super Meat Boy")


	def update(self, player, level):
		if not player.alive:
			player.deaths += 1
			player.move_to(level.spawn[0], level.spawn[1])
			player.alive = True

		state = pygame.key.get_pressed()
		if state[pygame.K_a]:
			player.vx = -1
		if state[pygame.K_d]:
			player.vx = 1
		if not (state[pygame.K_a] or state[pygame.K_d]):
			player.vx = 0

		player.vy = min(4, player.vy+0.05)
		if player.grounded:
			player.vy = 0

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				if player.grounded and event.key == pygame.K_w:
					player.vy -= 4

		player.move_by(player.vx, player.vy)

		for block in level.blocks:
			if player.rect().colliderect(block):
				player.grounded = True
				break
			player.grounded = False

		if not player.rect().colliderect(self.screen.get_rect()):
			player.alive = False

		for enemy in level.enemies:
			if player.rect().colliderect(enemy):
				player.alive = False
			enemy.move_by(enemy.vx, enemy.vy)
			if enemy.y+enemy.h/2 > self.resolution[1]:
				enemy.y = enemy.h/2
			elif enemy.y+enemy.h/2 < 0:
				enemy.y = self.resolution[1]-enemy.h/2

		for goal in level.goals:
			if player.rect().colliderect(goal):
				player.won = True

	def draw(self, player, level):
		if player.won:
			win_label = self.font.render("You win!", 1, (255, 255, 0))
			self.screen.blit(win_label, (620, 320))
			pygame.display.flip()
			time.sleep(2)
			return level.num
		else:
			self.screen.fill((0, 0, 0))
			try:
				self.screen.blit(player.face, player.rect())
			except:
				pygame.draw.rect(self.screen, (200, 0, 0), player.rect())
			for block in level.blocks:
				pygame.draw.rect(self.screen, (128, 128, 128), block.rect())
			for enemy in level.enemies:
				pygame.draw.rect(self.screen, (255, 128, 0), enemy.rect())
			for goal in level.goals:
				pygame.draw.rect(self.screen, (0, 255, 0), goal.rect())
			control_label = self.font.render("Use WASD to move. Avoid the enemies and make it to the goal!", 1, (255, 255, 255))
			self.screen.blit(control_label, (16, 16))
			death_label = self.font.render(str(player.deaths)+(" Death" if player.deaths == 1 else " Deaths"), 1, (0, 255, 255))
			self.screen.blit(death_label, (16, 684))
			return 0


def main(argv):
	pygame.init()
	size = (1280, 720)
	camera = Camera(0)
	font = pygame.font.SysFont("monospace", 16)
	game_object = Game(size, camera, font)
	level = level1
	player = MeatBoy(pos = level.spawn)
	player.face = game_object.camera.find_face(player.size())
	game_object.camera.close()

	while 1:
		game_object.update(player, level)
		retval = game_object.draw(player, level)
		pygame.display.flip()
		if retval == 1:
			level = level2
			player, player.face = MeatBoy(pos = level.spawn), player.face
		elif retval == 2:
			sys.exit()
		time.sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(sys.argv)
