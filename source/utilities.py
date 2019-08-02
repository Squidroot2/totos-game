"""Contains miscellaneous utility functions

Functions:
    readINI(config_path) : Takes the location of the config and returns a ConfigParser object containg the contents
    loadJson(json_path) : Takes the location of the json file and returns a dictionary containing the contents
    getItemById(json_path, id, category=None) : Returns a dictionary containing the particular information from the json file
    getDistanceBetweenEntities(coordsA, coordsB) : Takes two coordinates and returns the distance between them
    terminateGame() : Quits the program
    checkForQuit() : Terminates the game if the QUIT event is present or the Escape key has been pressed
"""


import configparser, sys, json
import pygame
from pygame.constants import *


def readINI(config_path):
    """Takes the location of the config and returns a ConfigParser object containing the contents
    
    *Currently Unused*
    
    Parameters:
        config_path : string
    
    Returns:
        config : configparser.ConfigParser : Contains the data pulled from the file at the config_path
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def loadJson(json_path):
    """Takes the location of the json file and returns a dictionary containing the contents
    
    Parameters: 
        json_path : string : location of the file being loaded
    
    Returns:
        : dict : contains data from the json file
        """
    with open(json_path) as json_file:
        return json.load(json_file)


def getDistanceBetweenEntities(coordsA, coordsB):
    """Gets the distance betweeen two points on a map
    
    Different from euclidean distance in that diagonal distance = 1
    
    Parameters:
        coordsA : tuple of 2 ints 
        coordsB : tuple of 2 ints
    
    Returns : int
    """
    x_dis = abs(coordsA[0] - coordsB[0])
    y_dis = abs(coordsA[1] - coordsB[1])
    
    if x_dis > y_dis:
        return x_dis
    else:
        return y_dis


def getLineBetweenEntities(coordsA, coordsB):
    """Gets a path that represents a straight line between entities

    Parameters:
        coordsA : Tuple(int,int)
        coordsB : Tuple(int,int)

    Returns: List[Tuple(int,int)]"""

    dist = getDistanceBetweenEntities(coordsA, coordsB)

    path = list()

    for i in range(dist):
        x = int(coordsA[0] + (coordsB[0]-coordsA[0])/dist*(i+1))
        y = int(coordsA[1] + (coordsB[1]-coordsA[1])/dist*(i+1))
        path.append((x, y))

    return path

def terminateGame():
    """Quits the program"""
    pygame.quit()
    sys.exit()


def checkForQuit():
    """Terminates the game if the QUIT event is present or the Escape key has been pressed"""
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminateGame() # terminate if any QUIT events are present
