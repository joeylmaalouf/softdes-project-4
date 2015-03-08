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
	font = pygame.font.SysFont("monospace", 24)
	screen = pygame.display.set_mode((480, 480))
	folderpath = dirname(abspath(__file__))
	button = pygame.image.load(folderpath+"/../assets/button.png").convert_alpha()
	(w, h) = button.get_size()
	button = pygame.transform.scale(button, (240, int(240.0/w*h)/2))
	(w, h) = button.get_size()
	game1_label = font.render("Dot Shooter", 1, (255, 255, 255))
	game2_label = font.render("Game of Life", 1, (255, 255, 255))
	game3_label = font.render("Super Meat Boy", 1, (255, 255, 255))
	button1_rect = pygame.Rect(120, 100, w, h)
	button2_rect = pygame.Rect(120, 200, w, h)
	button3_rect = pygame.Rect(120, 300, w, h)

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				(x, y) = pygame.mouse.get_pos()
				if button1_rect.collidepoint(x, y):
					dot.main(argv)
				elif button2_rect.collidepoint(x, y):
					gol.main(argv)
				elif button3_rect.collidepoint(x, y):
					smb.main(argv)
		screen.blit(button, button1_rect)
		screen.blit(button, button2_rect)
		screen.blit(button, button3_rect)
		screen.blit(game1_label, (160, 116))
		screen.blit(game2_label, (150, 216))
		screen.blit(game3_label, (140, 316))
		pygame.display.flip()


if __name__ == "__main__":
	main(argv)
