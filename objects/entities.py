'''
Contains the classes used to construct actors(player,enemies,items)
'''
from objects.ai import AI
from scripts.constants import *
import os, pygame

# my modules
from objects.inventory import *


class Entity:
    image_path = os.path.join('images', 'unknown.png')

    def __init__(self,location,x=None,y=None,components=[],obstruct=False):
        self.x = x
        self.y = y
        self.location = location
        self.location.addEntity(self)
        self.obstruct = obstruct
        self.loadImage()

        if 'AI' in components:
            self.ai = AI(self)
        else:
            self.ai = None
        
        if 'Inventory' in components:
            self.inventory = Inventory(self, components['Inventory'])
        else:
            self.inventory = None

    def loadImage(self):
        self.image = pygame.image.load(self.image_path).convert_alpha()

    def draw(self, surface):
        """Takes a pygame surface object and blits the object's 'image' to it at the specified x and y coordinates"""
        surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))



class Corpse(Entity):
    """This is created when a character object has been killed"""
    def __init__(self, character):
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.location, character.x, character.y,  components={'Inventory': inventory_contents})
        
    # todo add image for corpse
    





