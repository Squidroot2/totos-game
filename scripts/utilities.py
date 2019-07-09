import configparser
import sys

import pygame


def readINI(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()