import configparser
import sys
import json

import pygame
from pygame.constants import *


def readINI(config_path):
    """Takes the location of the config and returns a ConfigParser object containing the contents"""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def loadJson(json_path):
    """Returns a dictionary after loading the json file at the specified location"""
    with open(json_path) as json_file:
        return json.load(json_file)

def getItemById(json_path, id, category=None):
    """Returns a Dictionary containing the particular information from the json file"""
    json_file = loadJson(json_path)
    if category is None:
        return json_file[id]
    else:
        return json_file[category][id]



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