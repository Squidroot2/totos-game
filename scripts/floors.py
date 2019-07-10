import os
import random

import pygame
import tcod

from scripts.characters import Character
from scripts.constants import CELL_WIDTH, CELL_HEIGHT


class Floor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = tcod.map.Map(width, height)
        self.tile_map = [[Tile(self.map, x, y) for y in range(height)] for x in range(width)]
        self.entities = []
        # primitive random generation
        for xtile in range(self.width):
            for ytile in range(self.height):
                roll_block = random.randint(0,9)
                if not roll_block == 0:
                    self.map.walkable[ytile][xtile] = True
                    self.map.transparent[ytile][xtile] = True
        self.updateTiles()
        self.generateEnemies(3)



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
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].draw(surface)

    def addEntity(self, entity):
        self.entities.append(entity)

    def removeEntity(self, entity):
        self.entities.remove(entity)


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
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'black-tile.png'))