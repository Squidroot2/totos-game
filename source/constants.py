"""
This module contains constants used throughout the game

Variables:
    WINDOW_HEIGHT : int
    WINDOW_WIDTH : int
    FLOOR_HEIGHT :int
    FLOOR_WIDTH : int
    CELL_SIZE : int
    COLORS : dictionary of 3-item tuples
    FONTS : dictioanry of pygame.Fonts
    FPS : int
"""
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
          'RED':        (255,  0,  0),
          'LIGHT BLUE': (100,255,255),
          'YELLOW':     (255,255,  0),
          'GOLDENROD':  (190,145, 20)}


pygame.font.init()
FONTS = {'TITLE': pygame.font.Font('freesansbold.ttf', 70),
         'MAIN': pygame.font.Font('freesansbold.ttf', 28),
         'SUBMAIN': pygame.font.Font('freesansbold.ttf', 20),
         'INFO': pygame.font.Font('freesansbold.ttf', 14),
         'LOG': pygame.font.Font('freesansbold.ttf', 12)}

FONTS['TITLE'].set_underline(True)
FPS = 60

BACKGROUNDS = ("Officer", "Marksman", "Agent", "Pointman", "Gladiator")