'''
This module contains constants used throughout the grim ranger game
'''
import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FLOOR_WIDTH = 40
FLOOR_HEIGHT = 40

CELL_SIZE = 32


#                         R   G   B
COLORS = {'BLACK':      (  0,  0,  0),
          'DARK GRAY':  ( 25, 25, 25),
          'WHITE':      (255,255,255),
          'RED':        (255,  0,  0)}


pygame.font.init()
FONTS = {'TITLE': pygame.font.Font('freesansbold.ttf', 70),
         'MAIN': pygame.font.Font('freesansbold.ttf', 28),
         'INFO': pygame.font.Font('freesansbold.ttf', 14),
         'LOG': pygame.font.Font('freesansbold.ttf', 12)}

FONTS['TITLE'].set_underline(True)
FPS = 144