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
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FLOOR_WIDTH = 35
FLOOR_HEIGHT = 35

CELL_SIZE = 32


#                         R   G   B
COLORS = {'BLACK':      (  0,  0,  0),
          'DARK GRAY':  ( 25, 25, 25),
          'GRAY':       ( 50, 50, 50),
          'LIGHT GRAY': (100,100,100),
          'WHITE':      (255,255,255),
          'RED':        (255,  0,  0),
          'LIGHT BLUE': (100,255,255),
          'YELLOW':     (255,255,  0),
          'DARK YELLOW':(175,175,  0),
          'ORANGE':     (255,165,  0),
          'GOLDENROD':  (190,145, 20),
          'BLUE':       (  0,  0,255)}

DRAW_ORDER =    {'CORPSE': 0,
                 'PORTAL': 1,
                 'ITEM': 2,
                 'ENEMY': 3,
                 'PLAYER': 4,
                 'TARGET': 5}

WEAPONS = {"PISTOL", "RIFLE", "PDW", "CANNON", "KNIFE", "CLUB", "SWORD"}
REACTORS = {"RECYCLE", "LIGHT", "MEDIUM", "HEAVY", "BRAWLER"}

pygame.font.init()
FONT_FILES = {'UNISPACE' : os.path.join('fonts', 'unispace_rg.ttf')}

FONTS = {'TITLE':       pygame.font.Font('freesansbold.ttf', 70),
         'MAIN':        pygame.font.Font('freesansbold.ttf', 28),
         'SUBMAIN':     pygame.font.Font('freesansbold.ttf', 20),
         'INFO_HEADER': pygame.font.Font(FONT_FILES['UNISPACE'], 16),
         'INFO':        pygame.font.Font(FONT_FILES['UNISPACE'], 14),
         'INFO_S':      pygame.font.Font(FONT_FILES['UNISPACE'], 12),
         'LOG':         pygame.font.Font('freesansbold.ttf', 12)}

FONTS['TITLE'].set_underline(True)
FPS = 144

BACKGROUNDS = ("Officer", "Marksman", "Agent", "Pointman", "Gladiator")