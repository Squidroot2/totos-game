"""Contains classes for the overall game

Classes:
    Game : Stores high level game information
    Log : Keeps track of game messages
"""
# Standard Library
import os
from collections import Counter
# Third-Party
import pygame
# My Modules
from source.constants import CELL_SIZE, FLOOR_WIDTH, FLOOR_HEIGHT
from source.utilities import smartSplit



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
        self.surface = pygame.Surface((FLOOR_WIDTH*CELL_SIZE, FLOOR_HEIGHT*CELL_SIZE))

    def removeSurfaces(self):
        """Removes all images so that the game can be pickled (saved)"""
        for floor in self.dungeon:
            for entity in floor.entities:
                entity.image = None
                if entity.inventory:
                    for item in entity.inventory.contents:
                        item.image = None
            for x in range(FLOOR_WIDTH):
                for y in range(FLOOR_HEIGHT):
                    floor.tile_map[x][y].image = None

            if floor.chest.item:
                floor.chest.item.image = None

        self.surface = None

    def setSurfaces(self):
        """Gets the surfaces back after loading the save"""
        for floor in self.dungeon:
            for entity in floor.entities:
                entity.setImage()
                if entity.inventory:
                    for item in entity.inventory.contents:
                        item.setImage()
            for x in range(FLOOR_WIDTH):
                for y in range(FLOOR_HEIGHT):
                    floor.tile_map[x][y].setImage()

            if floor.chest.item:
                floor.chest.item.setImage()

        self.surface = pygame.Surface((FLOOR_WIDTH*CELL_SIZE, FLOOR_HEIGHT*CELL_SIZE))
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
        getLastMessage(self, lines) : Gets a specified number of messages from the end of the messages list
        addEOTUnderscore(self) : Adds an underscore to the last message of the turn
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
        self.buffer = []
        self.setInstance(self)

    def getLastLines(self, lines, max_length):
        """Gets a specified number of lines of messages from the end of the messages list

        Parameters:
            lines : int
            max_length : int

        Returns: List[string]
        """
        last_messages = []

        for message in self.messages[-lines:]:
            if len(message) > max_length:
                last_messages.extend(smartSplit(message, max_length))
            else:
                last_messages.append(message)

        return last_messages[-lines:]

    def addEOTUnderscore(self):
        """Adds an underscore to the last message of the turn"""
        # Only adds the underscore if the last character of the last message is not an underscore
        if self.messages[-1][-1] != "_":
            self.messages[-1] = self.messages[-1] + "_"

    def write(self):
        """Adds the messages in the buffer to the messages list"""
        # Condense the Buffer Using a Counter
        buffer_counter = Counter(self.buffer)
       
        # For every message in the buffer_counter object...
        for message in buffer_counter:
            
            # If the number of occurrences(N) is greater than 1, add " xN" to message
            if buffer_counter[message] > 1:
                message += " x%d" % buffer_counter[message]
            
            # Add the message to the list of messages
            self.messages.append(message)
        
        # Clear the buffer
        self.buffer = []

    @classmethod
    def addToBuffer(cls, message):
        """Adds messages to the buffer"""
        cls.instance.buffer.append(message)

    @classmethod
    def setInstance(cls, instance):
        """Used by the init function to keep track of the current instance in a class attribute"""
        cls.instance = instance

    @classmethod
    def addMessage(cls, message):
        """Used by external functions to add messages to the current instance"""
        cls.instance.messages.append(message)
