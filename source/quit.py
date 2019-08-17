"""Contains functions for quitting and saving the game"""

import sys
import pickle
import os

import pygame
from pygame.constants import QUIT

SAVE_LOCATION = os.path.join('saves', 'totos.save')

def loadSave():
    """Loads the save from the save location then sets the surfaces"""
    with open(SAVE_LOCATION, 'rb') as file:
        game = pickle.load(file)

    game.setSurfaces()
    return game


def terminateGame(game=None):
    """Quits the program"""
    if game is not None:  # Save the game
        # Strip the game of surfaces
        game.removeSurfaces()

        # Create Folder if it doesn't exit
        if not os.path.exists('saves'):
            os.makedirs('saves')

        # Pickle dump the game
        with open(SAVE_LOCATION, 'wb') as file:
            pickle.dump(game, file)

    pygame.quit()
    sys.exit()


def checkForQuit(game=None):
    """Terminates the game if the QUIT event is present or the Escape key has been pressed"""
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminateGame(game) # terminate if any QUIT events are present
