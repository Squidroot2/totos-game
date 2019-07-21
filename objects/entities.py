"""
Contains the classes used to construct actors(player,enemies,items)

Classes:
    Entity
    Target(Entity)
    Portal(Entity)
    Corpse(Entity)
"""

import os, pygame

from objects.ai import AI
from objects.inventory import *
from scripts.constants import CELL_SIZE


class Entity:
    """Represents any object that can act and be drawn into the world
    
    Attributes:
        image_path : string
            CLASS; Used to identify relative location of the image file
        CELL_SIZE : int
            CLASS; The number of pixels in the width and height of each image
        x : int or None
            X location on the tile map. Should be None if not on a tile map
        y : int or None
            Y location on the tile map. Should be None if not on a tile map
        location : Floor or Inventory
            where the entity is found in the game
        obstruct : bool
            Whether the entity stops another entity from moving through it.
            Typically, Characters should have this set to true and everything else should be false
        image : pygame.Surface
            the entity's image as a Surface object
        ai : AI or None
            the entity's AI component if it has one
        inventory : Inventory or None
            the entity's Inventory component if it has one
    
    Methods:
        loadImage(self) : Loads the image stored at the image_path attribute
        draw(self) : Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates
    
    Children:
        Corpse(Entity)
        Item(Entity)
            Armor(Item)
            Weapon(Item)
            Armor(Item)
            Battery(Item)
        Character(Entity)
            Player(Character)
    """
    
    # Default image_path value for all entities
    image_path = os.path.join('images', 'unknown.png')
    CELL_SIZE = CELL_SIZE

    def __init__(self, location, x=None, y=None, ai=None, inventory=None, obstruct=False, is_player=False):
        """Init method for Entity
        
        Parameters: 
            location : Floor or Inventory
                where the entity is found in the game
            x : int
                X location on the tile map. Should be None if not on a tile map
            y : int
                Y location on the tile map. Should be None if not on a tile map
            ai : None or True
            inventory : None or List
            obstruct : bool
                Whether the entity obtructs movement or not
        """
        self.x = x
        self.y = y
        self.location = location
        self.location.addEntity(self)
        self.obstruct = obstruct
        self.image = None
        self.discovered = False
        self.last_known_x = None
        self.last_known_y = None
        if is_player:
            self.is_player = True
        else:
            self.is_player = False

        if ai:
            self.ai = AI(self, ai)
        else:
            self.ai = None
        
        if inventory is not None:
            self.inventory = Inventory(self, inventory)
        else:
            self.inventory = None

    def loadImage(self):
        """Loads the image stored at the image_path attribute

        Requires pygame to be initialized"""
        self.image = pygame.image.load(self.image_path).convert_alpha()

    def draw(self, surface):
        """Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates

        Requires pygame to be initialized

        Paramaters:
            surface : pygame.Surface
                The surface that the image will get written to
        """
        # First load the image if it hasn't been loaded
        if self.image is None:
                self.loadImage()
        surface.blit(self.image, (self.x*self.CELL_SIZE, self.y*self.CELL_SIZE))

    def drawAtLastKnown(self, surface):
        """Draws the entity at the last known location rather than necessarily the actual location"""
        surface.blit(self.image, (self.last_known_x*self.CELL_SIZE, self.last_known_y*self.CELL_SIZE))


# todo finish Target  class
class Target(Entity):
    # todo give Target an image or draw method
    """Represents the player's target when aiming or exploring"""
    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

class Portal(Entity):
    """Entity used to move player between floors"""

    def __init__(self, location, x, y, direction):
        super().__init__(location, x, y)
        assert direction in ("up", "down")
        if direction == "down":
            self.image_path = os.path.join('images', 'other', 'down_portal.png')
        else:
            self.image_path = os.path.join('images', 'other', 'up_portal.png')
        self.direction = direction


class Corpse(Entity):
    """This is created when a character object has been killed
    
    Child of Entity
    
    Attributes:
        image_path : string
            INHERITED, CLASS; Used to identify relative location of the image file
        CELL_SIZE : int
            INHERITED, CLASS; The number of pixels in the width and height of each image
        x : int or None
            INHERITED; X location on the tile map. Should be None if not on a tile map
        y : int or None
            INHERITED; Y location on the tile map. Should be None if not on a tile map
        location : Floor
            INHERITED; what floor the corpse is found in the game
        obstruct : bool
            INHERITED; Whether the entity stops another entity from moving through it. 
            Should be False for Corpses
        image : pygame.Surface
            INHERITED; the corpse's image as a Surface object
        ai : None
            INHERITED; Specifies that corpse does not have ai
        inventory : Inventory
            INHERITED; the corpse's Inventory component
    """

    image_path = os.path.join('images', 'other', 'headstone.png')
    def __init__(self, character):
        """Init method for Corpse. Extends the init method of Entity
        
        
        Parameters:
            character : Character
                The character that died this is make this corpse
        """
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.location, character.x, character.y, inventory=inventory_contents)
        
    # todo add image for corpse
    





