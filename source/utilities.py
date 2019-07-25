"""Contains miscellaneous utility functions

Functions:
    readINI(config_path) : Takes the location of the config and returns a ConfigParser object containg the contents
    loadJson(json_path) : Takes the location of the json file and returns a dictionary containing the contents
    getItemById(json_path, id, category=None) : Returns a dictionary containing the particular information from the json file
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


def getItemById(json_path, id, category=None):
    """Returns a Dictionary containing the particular information from the json file
    
    Parameters:
        json_path : string : location of the file being loaded
        id : string : id of the item in the file
        category : None or string : For files that have categories, specifies item
    
    Returns:
        : dict : contains only the data associated with the specified item
    """
    json_file = loadJson(json_path)
    if category is None:
        return json_file[id]
    else:
        return json_file[category][id]

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
        

def terminateGame():
    """Quits the program"""
    pygame.quit()
    sys.exit()

def checkForQuit():
    """Terminates the game if the QUIT event is present or the Escape key has been pressed"""
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminateGame() # terminate if any QUIT events are present
