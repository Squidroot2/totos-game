"""Contains classes for the overall game

Classes:
    Game : Stores high level game information
    Log : Keeps track of game messages
"""
import pygame
from scripts.constants import CELL_SIZE, FLOOR_WIDTH, FLOOR_HEIGHT


class Game:
    """Stores high level game information

    Attributes:
        dungeon: List of Floor
        player: Player
        log: Log
            Keeps track of things that happen in the game; created in the init method
        surface : pygame.Surface
            Objects in the game are drawn to here, then this is blitted to the main window
    """
    def __init__(self, dungeon, player):
        """Init method for Game

        Parameters:
            dungeon: list of Floor objects
            player: Player object
        """
        self.dungeon = dungeon
        self.player = player
        self.log = Log(self)
        self.surface = pygame.Surface((FLOOR_WIDTH*CELL_SIZE,FLOOR_HEIGHT*CELL_SIZE))
        


class Log:
    """Keeps track of game information. Is used to print output to the screen

    Attributes:
        instance: Log
            CLASS; stores the current instance in the class so that access to the class grants access to the instance
        game : Game
            The current Game
        messages : List of strings
            Stores  messages to be drawn to the screen
    Methods:
        getLastMessage(self, num) : Gets a specified number of messages from the end of the messages list
        setInstance(cls, instance) : CLASS; Used by the init function to keep track of the current instance in a class
            attribute
        addMessage(cls, message) : CLASS; Used by external functions to add messages to the current instance
        """
    instance = None
    def __init__(self, game):
        """Init method for Log

        Parameters:
            game : Game
                The current game
        """
        self.game = game
        # Starts off with a welcome message
        self.messages = ["Welcome to the Dungeon, " + self.game.player.name]
        self.setInstance(self)

    def getLastMessages(self, num):
        """Gets a specified number of messages from the end of the messages list"""
        return self.messages[-num:]

    def addEOTUnderscore(self):
        """Adds an underscore to the last message of the turn"""
        self.messages[-1] = self.messages[-1] + "_"

    @classmethod
    def setInstance(cls, instance):
        """Used by the init function to keep track of the current instance in a class attribute"""
        cls.instance = instance

    @classmethod
    def addMessage(cls, message):
        """Used by external functions to add messages to the current instance"""
        cls.instance.messages.append(message)