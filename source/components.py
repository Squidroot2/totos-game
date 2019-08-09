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
from source.constants import CELL_SIZE, BACKGROUNDS
from source.utilities import getDistanceBetweenEntities
from source.assets import Data



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
        assert ai_type in ("basic", "brainless", "ranger", "fencer")
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
                    distance = getDistanceBetweenEntities((self.owner.x, self.owner.y), (self.opponent.x, self.opponent.y))

                    # If Outside Range or not within fov or not enough energy to take shot
                    if distance > self.owner.getRange()  or not self.owner.location.map.fov[self.owner.y][self.owner.x] \
                            or self.owner.getEnergyPerShot() > self.owner.energy:
                        self.moveNextToEntity(self.opponent)

                    # If within 1 tile, melee attack
                    elif distance == 1:
                        self.owner.attack(self.opponent, is_ranged=False)

                    # Otherwise perform ranged attack
                    else:
                        self.owner.attack(self.opponent, is_ranged=True)

            elif self.type == "fencer":
                if self.owner.location is self.opponent.location:

                    if self.owner.energy > 0:
                        if getDistanceBetweenEntities((self.owner.x, self.owner.y), (self.opponent.x, self.opponent.y)) > 1:
                            self.moveNextToEntity(self.opponent)
                        else:
                            self.owner.attack(self.opponent, is_ranged=False)

                    # If fencer is out of energy, tries to run, If it can't, it attacks
                    else:
                        can_run = self.moveAwayFromEntity(self.opponent)
                        if not can_run and getDistanceBetweenEntities((self.owner.x, self.owner.y), \
                                                                      (self.opponent.x, self.opponent.y)) == 1:
                            self.owner.attack(self.opponent, is_ranged=False)



    def moveNextToEntity(self, target):
        """Moves peacefully toward the specified entity"""
        path = self.owner.location.path_finder.get_path(self.owner.x, self.owner.y, target.x, target.y)
        next_move = path[0]
        x_move = next_move[0] - self.owner.x
        y_move = next_move[1] - self.owner.y

        self.owner.move(x_move, y_move, peacefully=True)

    def moveAwayFromEntity(self, target):
        """Attempts to move away from the target"""

        attemptMove = self.owner.move

        # Simply try to move directly away from the target
        delta_move_x = self.owner.x - target.x
        delta_move_y = self.owner.y - target.y

        distance = getDistanceBetweenEntities((self.owner.x, self.owner.y), (target.x, target.y))

        if distance > 1:
            # Ensures the target does not try to move more than 1 space
            if delta_move_x > 0:
                delta_move_x = 1
            elif delta_move_x < 0:
                delta_move_x = -1

            if delta_move_y > 0:
                delta_move_y = 1
            elif delta_move_y < 0:
                delta_move_y = -1

        assert(delta_move_y) in (-1, 0, 1)
        assert(delta_move_x) in (-1, 0, 1)

        did_move = attemptMove(delta_move_x, delta_move_y, peacefully=True)

        if did_move:
            return True
        else:
            # If attempting vertical movement, attempt diagonals in same y direction
            if delta_move_x == 0:
                for x in (-1, 1):
                    did_move = attemptMove(x, delta_move_y, peacefully=True)
                    if did_move:
                        return True
                # Try to make lateral movements as long as the target is not in melee range
                if distance != 1:
                    for x in (-1, 1):
                        did_move = attemptMove(x, 0, peacefully=True)
                        if did_move:
                            return True

                # All Attempts Failed, Return False
                return False

            # If attempting horizontal movement, attempt diagonals in same x direction
            elif delta_move_y == 0:
                for y in (-1, 1):
                    did_move = attemptMove(delta_move_x, y, peacefully=True)
                    if did_move:
                        return True

                # Try to make lateral movements as long as the target is not in melee range
                if distance != 0:
                    for y in (-1, 1):
                        did_move = attemptMove(0, y, peacefully=True)
                        if did_move:
                            return True

                # All Attempts Failed; Return False
                return False

            # If Attempting diagonals, attempt all movements that maintain either x direction or y direction
            else:
                # Moves that maintain y direction
                for x in (-1, 0, 1):
                    # No need to retry what has been tried
                    if x == delta_move_x:
                        continue
                    did_move = attemptMove(x, delta_move_y, peacefully=True)
                    if did_move:
                        return True
                # Moves that maintain x direction
                for y in (-1, 0, 1):
                    # No need to retry what has been tried
                    if y == delta_move_y:
                        continue
                    did_move = attemptMove(delta_move_x, y, peacefully=True)
                    if did_move:
                        return True

                # All Attempts Failed; Return False
                return False

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
    def __init__(self, owner, inv_type):

        # Type Validation
        type_is_valid = inv_type in ('empty', 'BOXER') or inv_type in BACKGROUNDS
        assert type_is_valid

        self.owner = owner
        self.contents = []
        self.contents_condensed = []
        self.equipped = {"weapon": None, "armor": None, "reactor": None}

        # If the inventory type is not empty, get the inventory data and create the items.
        if inv_type != "empty":
            self.populate(inv_type)

            # Set the reactor to full energy if there is one equipped
            if self.equipped['reactor'] is not None:
                self.equipped['reactor'].rechargeToFull()

    def populate(self, inv_type):
        """Populates the inventory with the intial items using the inventory type"""
        # Imports occurs here to avoid dependency loop with the entities module
        from source.entities import Item

        # Get either a player background inventory or a leveled inventory
        if inv_type in BACKGROUNDS:
            data = Data.getPlayerInventory(inv_type)
        else:
            data = Data.getInventory(inv_type, self.owner.level)

        # Create Equipped items
        for slot in self.equipped:
            if data[slot] is not None:
                self.equipped[slot] = Item.createItem(data[slot], self)

        # Other is a list of items which are not equipped
        if data['other'] is not None:
            for item_id in data['other']:
                Item.createItem(item_id, self)

    def addEntity(self, item):
        self.contents.append(item)

    def removeEntity(self, item):
        self.contents.remove(item)

    def dropAll(self):
        """Drops all items in the inventory. Called when the owner dies"""
        for slot in self.equipped:
            self.equipped[slot] = None
        for item in self.contents:
            item.drop()
    
    # todo create condenseInventory method
    def condenseInventory(self):
        pass
        
    # todo create a method that returns a condensed dictionary of items of a specified type
    def getItemsOfType(self, type):
        pass
    

