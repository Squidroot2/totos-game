'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.constants import *
import os, pygame, random

class Entity():
    image = pygame.image.load(os.path.join('images', 'unknown.png'))

    def __init__(self,x,y):
        self.x = x
        self.y = y



    def draw(self, surface):
        if not self.dead:
            surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))

class Character(Entity):
    dead = False


    def move(self, game_map, delta_x, delta_y):
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(game_map, destination):
            if not self.attack(game_map, destination):
                self.x += delta_x
                self.y += delta_y

    def validateMove(self, game_map, destination):
        # If destination is out of range
        if destination[0] < 0 or destination[0] >= game_map.width:
            return False
        elif destination[1] < 0 or destination[1] >= game_map.height:
            return False
        # If destination is blocked
        elif game_map.tile_map[destination[0]][destination[1]].block_path:
            return False
        else:
            return True

    def attack(self, game_map, destination):
        for entity in game_map.entities:
            if entity.x == destination[0] and entity.y == destination[1]:
                entity.kill()
                print("ATTACK")
                return True
            else:
                return False

    def kill(self):
        self.dead = True

class Player(Character):
    image = pygame.image.load(os.path.join('images','characters','player.png'))

class Enemy(Character):
    image = pygame.image.load(os.path.join('images','characters','enemy.png'))

    def randomMove(self, game_map):
        x_move = random.randint(-1,1)
        y_move = random.randint(-1,1)
        self.move(game_map, x_move, y_move)


#todo write items class(es)

