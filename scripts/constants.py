'''
This module contains constants used throughout the grim ranger game
'''

import pygame
FPS = 30

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

MAP_WIDTH = 39
MAP_HEIGHT = 22

CELL_WIDTH = 32
CELL_HEIGHT = 32

#                    R   G   B
COLORS = {'BLACK': (  0,  0,  0),
          'WHITE': (255,255,255)}

BG_COLOR = COLORS['BLACK']

pygame.font.init()
FONTS = {'TITLE': pygame.font.Font('freesansbold.ttf', 70),
         'MAIN': pygame.font.Font('freesansbold.ttf', 28)}

FONTS['TITLE'].set_underline(True)