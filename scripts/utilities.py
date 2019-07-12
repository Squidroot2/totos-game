import configparser
import sys

import pygame
from pygame.constants import *


def readINI(config_path):
    """Takes the location of the config and returns a ConfigParser object containing the contents"""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()

def checkForQuit():
    """Terminates the game if the QUIT event is present or the Escape key has been pressed"""
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminateGame() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYDOWN): # get all the KEYDOWN events
       if event.key == K_ESCAPE:
          terminateGame() # terminate if the KEYDOWN event was for the Esc key
       pygame.event.post(event) # put the other KEYDOWN event objects back