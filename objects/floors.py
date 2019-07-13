import os
import random

import pygame
import tcod

from objects.characters import Character
from scripts.constants import CELL_WIDTH, CELL_HEIGHT


class Floor:
    MAP_WIDTH = 39
    MAP_HEIGHT = 22
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = tcod.map.Map(width, height)
        self.tile_map = [[Tile(self.map, x, y) for y in range(height)] for x in range(width)]
        self.entities = []
        # # primitive random generation
        # for xtile in range(self.width):
        #     for ytile in range(self.height):
        #         roll_block = random.randint(0,9)
        #         if not roll_block == 0:
        #             self.map.walkable[ytile][xtile] = True
        #             self.map.transparent[ytile][xtile] = True
        self.generateLayout()
        self.updateTiles()
        self.generateEnemies(3)

    def generateLayout(self):

        bsp = tcod.bsp.BSP(0,0,self.width-1,self.height-1)
        bsp.split_recursive(depth=5,min_width=3,min_height=3,max_horizontal_ratio=2,max_vertical_ratio=2)
        for node in bsp.pre_order():
            if node.children:
                self.makeHallway(node)

            else:
                self.makeRoom(node)

    def makeHallway(self,node):
        if node.horizontal:
            y = node.position
            x = random.randint(node.x+1, node.x + node.width-1)
        else:
            x = node.position
            y = random.randint(node.y+1, node.y + node.height-1)

        self.map.transparent[y][x] = True
        self.map.walkable[y][x] = True

    def makeRoom(self,node):
        x = node.x + 1
        y = node.y + 1
        width = node.width - 1
        height = node.height - 1

        for a in range(height):
            for b in range(width):
                self.map.transparent[y+a][x+b] = True
                self.map.walkable[y+a][x+b] = True

    def generateEnemies(self, number_of_enemies):
        for enemy in range(number_of_enemies):
            x = random.randint(0, self.width -1)
            y = random.randint(0, self.height -1)
            Character("BLOB1",self, x, y, ['AI'])

    def updateTiles(self):
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].update(self.map)

    def draw(self, surface):
        """Draws all of the tiles in the tile map at the appropriate location

        Parameters:
            surface : pygame.Surface
                surface to draw to
        """
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].draw(surface)

    def addEntity(self, entity):
        """Adds an entity to the entities list attribute

        Parameters:
            entity : Entity
                entity to add
        """
        self.entities.append(entity)

    def removeEntity(self, entity):
        """Removes an entity from the entities list attribute"""
        self.entities.remove(entity)

    @classmethod
    def generateDungeon(cls, floors):
        """Returns a list of a specified number of floors

        Parameters:
            floors : int
                number of floors in the dungeon
        """
        floor_list = list()

        for index in range(floors):
            floor_list.append(Floor(cls.MAP_WIDTH, cls.MAP_HEIGHT))

        return floor_list



class Tile:
    def __init__(self, map, x, y):
        # Row Major Order
        self.walkable = map.walkable[y][x]
        self.transparent = map.transparent[y][x]
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT))

    def update(self, map):
        self.walkable = map.walkable[self.y][self.x]
        self.transparent = map.transparent[self.y][self.x]
        if self.walkable and self.transparent:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'white-tile.png'))
        else:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'wall.png'))