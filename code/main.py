""" A multi-game arcade
	in Python.
"""
import pygame
from os.path import abspath, dirname
from sys import argv, exit

import dot
import gol
import smb


def main(argv):
	pygame.init()
	font = pygame.font.SysFont("monospace", 16)
	screen = pygame.display.set_mode((480, 480))
	folderpath = dirname(abspath(__file__))
	button = pygame.image.load(folderpath+"/../assets/button.png").convert_alpha()
	(w, h) = button.get_size()
	button = pygame.transform.scale(button, (240, int(240.0/w*h)/2))


	while 1:
		screen.blit(button, (120, 100))
		screen.blit(button, (120, 200))
		screen.blit(button, (120, 300))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit()


if __name__ == "__main__":
	main(argv)
