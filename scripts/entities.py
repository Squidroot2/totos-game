'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.ai import AI
from scripts.constants import *
import os, pygame

# my modules
from scripts.inventory import *


class Entity:
    image = pygame.image.load(os.path.join('images', 'unknown.png'))
    
    # todo rearrange signature so that location is first, amd x and y are optional
    def __init__(self,location,x=None,y=None,components=[]):
        self.x = x
        self.y = y
        self.location = location
        self.location.addEntity(self)
        obstruct = False

        if 'AI' in components:
            self.ai = AI(self)
        else:
            self.ai = None
        
        if 'Inventory' in components:
            self.inventory = Inventory(self, components['Inventory'])
        else:
            self.inventory = None

    def draw(self, surface):
        surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))



class Corpse(Entity):
    def __init__(self, character):
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.location, character.x, character.y,  components={'Inventory': inventory_contents})
        
    # todo add image for corpse
    





