'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.constants import *
import os

class Entity():
    image = os.path.join('images', 'unknown.png')

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def draw(self, surface):
        surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))

class Character(Entity):
    def move(self, game_map, delta_x, delta_y):
        if not game_map[self.x + delta_x][self.y + delta_y].block_path:
            self.x += delta_x
            self.y += delta_y



#todo Write enemy class
class Enemy(Character):
    pass

#todo write player class
class Player(Character):


#todo write items class(es)

