import configparser
import sys

import pygame
from pygame.constants import *


def readINI(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminateGame() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
       if event.key == K_ESCAPE:
          terminateGame() # terminate if the KEYUP event was for the Esc key
       pygame.event.post(event) # put the other KEYUP event objects back