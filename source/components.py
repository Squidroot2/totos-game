"""Contains objects which act as components of Entities

Classes:
    AI
    Camera
    Inventory
"""
# Standard Library
import random
# Third Party
import pygame
# My Modules
from source.constants import CELL_SIZE
from source.utilities import getDistanceBetweenEntities


class AI:
    """Component Class for Characters

    Attributes:
        owner : Character
        type : string in ("basic","brainless")
        opponent : Player or None: Stores the player here when it is found

    Methods:
        findPlayer(self) : Searches through the list of entites in the location to find the player
        takeTurn(self) : Runs through conditional statements to determine how the AI will act this turn
        moveNextToEntity(self, target) :
        randomMove(self) : Moves randomly no more than 1 tile
    """
    def __init__(self, owner, ai_type):
        self.owner = owner
        assert ai_type in ("basic", "brainless")
        self.type = ai_type
        self.opponent = None

    def findPlayer(self):
        """Searches through the list of entities in the location to find the player"""
        for entity in self.owner.location.entities:
            if entity.is_player:
                return entity
        return None

    def takeTurn(self):
        """Runs through conditional statements to determine how the AI will act this turn"""
        if self.opponent is None:
            self.opponent = self.findPlayer()

        # If the entity is not discovered move around peacefully
        if not self.owner.discovered:
            self.randomMove(peacefully=True)

        # Otherwise, move based on ai type
        else:
            # Brainless AI
            if self.type == "brainless":
                self.randomMove()

            # Basic AI decisions
            elif self.type == "basic":
                # If the ai owner and the player are on the same floor
                if self.owner.location is self.opponent.location:
                    if getDistanceBetweenEntities((self.owner.x, self.owner.y), (self.opponent.x, self.opponent.y)) > 1:
                        self.moveNextToEntity(self.opponent)
                    else:
                        self.owner.attack(self.opponent, is_ranged=False)

                # If the ai owner is on a different floor
                else:
                    self.randomMove(peacefully=True)

            elif self.type == "ranger":
                # If the ai owner and the player are on the same floor...
                if self.owner.location is self.opponent.location:

                    # Move closer if out of range
                    if getDistanceBetweenEntities((self.owner.x, self.owner.y), (self.opponent.x, self.opponent.y)) \
                            > self.owner.getRange():
                        self.moveNextToEntity(self.opponent)

                    # If within range, attack
                    # todo make it so character must have LOS
                    else:
                        self.owner.attack(self.opponent, is_ranged=True)

    def moveNextToEntity(self, target):
        """Moves peacefully toward the specified entity"""
        path = self.owner.location.path_finder.get_path(self.owner.x, self.owner.y, target.x, target.y)
        next_move = path[0]
        x_move = next_move[0] - self.owner.x
        y_move = next_move[1] - self.owner.y

        self.owner.move(x_move, y_move, peacefully=True)

    def randomMove(self, peacefully=False):
        """Choose a random x and y movement. Could be (0,0)

        Parameters:
            peacefully : bool : passed to the Character.move() method
        """
        x_move = random.randint(-1, 1)
        y_move = random.randint(-1, 1)
        self.owner.move(x_move, y_move, peacefully)


class Camera:
    """Used for display the part of the game surface centered on a particular entity such as the player

    Attrbutes:
        width : int : CLASS; numbers of tiles wide
        height : int : CLASS; numbers of tiles tall

    Methods:
        update(self) : Updates the center of the camera based on the location of the owner
        getRect(self) : Returns the rectangle representing the camera in pixel dimensions
    """
    width = 29
    height = 21

    def __init__(self, owner):
        """Camera init function

        Parameters:
            owner : Entity
        """

        self.owner = owner
        self.center = (self.owner.x, self.owner.y)
        self.pixel_width = self.width * CELL_SIZE
        self.pixel_height = self.height * CELL_SIZE
        self.pixel_center = None
        self.update()

    def update(self):
        """Updates the center of the camera based on the location of the owner"""
        self.pixel_center = (self.owner.x*CELL_SIZE+.5*CELL_SIZE, self.owner.y*CELL_SIZE+.5*CELL_SIZE)
        self.center = (self.owner.x, self.owner.y)

    def getRect(self):
        """Returns the rectanlge representing the camera in  pixel dimensions

        Returns:
            rect : pygame.Rect
        """
        rect = pygame.Rect(0, 0, self.pixel_width, self.pixel_height)
        rect.center = self.pixel_center
        return rect

    def getTileRect(self):
        """Returns the rectangle representing the camera in tile dimensions"""
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.center
        return rect


class Inventory:
    ''' Component Class'''
    def __init__(self, owner, contents=[]):
        self.owner = owner
        self.contents = contents
        self.equipped = {"weapon": None, "armor": None, "generator": None}

    def addEntity(self, item):
        self.contents.append(item)

    def removeEntity(self, item):
        self.contents.remove(item)