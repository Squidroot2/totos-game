'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.constants import *
import os, pygame, random

# my modules
from scripts.inventory import *


class Entity():
    image = pygame.image.load(os.path.join('images', 'unknown.png'))
    
    # todo rearrange signature so that location is first, amd x and y are optional
    def __init__(self,x,y,location,components=[]):
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

# todo move characters to seperate modules


class Corpse(Entity):
    def __init__(self, character):
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.x, character.y, character.location, components={'Inventory': inventory_contents})
        
    # todo add image for corpse
    
    


# todo seperate to seperate module
class AI:
    '''Component Class'''
    def __init__(self, owner):
        self.owner = owner

    def takeTurn(self):
        self.randomMove()

    def randomMove(self):
        x_move = random.randint(-1,1)
        y_move = random.randint(-1,1)
        self.owner.move(x_move, y_move)




