'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.constants import *
import os

class Actor():
    image = os.path.join('images', 'unknown.png')

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def draw(self, surface):
        surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))

class Character(Actor):
    def move(self, game_map, delta_x, delta_y):
        if not game_map[self.x + delta_x][self.y + delta_y].block_path:
            self.x += delta_x
            self.y += delta_y



#todo Write enemy class

#todo write player class

#todo write items class(es)

