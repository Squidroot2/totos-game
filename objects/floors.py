import os
import random

import pygame
import tcod

from objects.entities import Portal
from objects.characters import Character
from scripts.constants import CELL_SIZE, FLOOR_HEIGHT, FLOOR_WIDTH


class Floor:
    width = FLOOR_WIDTH
    height = FLOOR_HEIGHT
    
    def __init__(self, floor_number):
        """Init method for the Floor class

        Parameters:
            floor_number : int
        """
        self.map = tcod.map.Map(self.width, self.height)
        self.tile_map = [[Tile(self.map, x, y) for y in range(self.height)] for x in range(self.width)]
        self.number = floor_number

        # Initialize empty variable
        self.entities = []
        self.rooms = []
        self.portals = {'up': None, 'down': None}
        self.landing_room = None

        # Random Generation of Floor
        self.generateLayout()
        self.updateTiles()
        self.generatePortals()
        self.generateEnemies()


    def generateLayout(self):
        """Uses Binary Space Partition to generate the layout of the dungeon"""
        bsp = tcod.bsp.BSP(0,0,self.width-1,self.height-1)
        bsp.split_recursive(depth=5,min_width=3,min_height=3,max_horizontal_ratio=2,max_vertical_ratio=2)
        for node in bsp.pre_order():
            if node.children:
                self.makeHallway(node)

            else:
                self.makeRoom(node)

    def makeHallway(self,node):
        """"Uses the properties of the given node to randomly create a hallway

        Parameters:
            node: tcod.bsp.BSP
        """
        if node.horizontal:
            y = node.position
            x = random.randint(node.x+1, node.x + node.width-1)
        else:
            x = node.position
            y = random.randint(node.y+1, node.y + node.height-1)

        self.map.transparent[y][x] = True
        self.map.walkable[y][x] = True

    def makeRoom(self,node):
        """Uses the properties of the given node to dig out a room

        Parameters:
            node : tcod.bsp.BSP
        """
        x = node.x + 1
        y = node.y + 1
        width = node.width - 1
        height = node.height - 1

        for a in range(height):
            for b in range(width):
                self.map.transparent[y+a][x+b] = True
                self.map.walkable[y+a][x+b] = True

        self.rooms.append({"x":x,"y":y,"w":width,"h":height})

    def generatePortals(self):
        """Creates up and down portals for the floor"""
        # Choose a random room
        up_room = random.choice(self.rooms)
        down_room = random.choice(self.rooms)
        while up_room is down_room:
            down_room = random.choice(self.rooms)

        for room in (up_room, down_room):
            if room is up_room:
                direction = "up"
            else:
                direction ="down"

            x = random.randrange(room['x'], room['x'] + room['w'])
            y = random.randrange(room['y'], room['y'] + room['h'])

            self.portals[direction] = Portal(self, x, y, direction)
            if direction == "up":
                self.landing_room = room


    def generateEnemies(self):
        """Generates a specified number of enemies for the floor

        Parameters:
            number_of_enemies: int
        """
        # todo allow multiple different types of enemies to be generated
        chance_per_room = .2

        for room in self.rooms:
            if room is self.landing_room:
                continue
            roll = random.random()
            if roll < chance_per_room:
                x = random.randrange(room['x'], room['x']+room['w'])
                y = random.randrange(room['y'], room['y']+room['h'])
                Character("BLOB1", self, x, y)


    def updateTiles(self):
        """Runs the update method on every tile in the tile_map"""
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

    @staticmethod
    def generateDungeon(num_of_floors):
        """Returns a list of a specified number of floors

        Parameters:
            num_of_floors : int
                number of floors in the dungeon
        """
        floor_list = list()

        for index in range(num_of_floors):
            floor_list.append(Floor(index+1))
            print(index)

        return floor_list


class Tile:
    CELL_SIZE = CELL_SIZE

    def __init__(self, map, x, y):
        # Row Major Order
        self.walkable = map.walkable[y][x]
        self.transparent = map.transparent[y][x]
        self.x = x
        self.y = y


    def draw(self, surface):
        """Blits the tile to the screen"""
        surface.blit(self.image, (self.x * self.CELL_SIZE, self.y * self.CELL_SIZE))

    def update(self, map):
        """Loads the image for each image depending on the values in the walkable and transparent array"""
        self.walkable = map.walkable[self.y][self.x]
        self.transparent = map.transparent[self.y][self.x]
        if self.walkable and self.transparent:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'white-tile.png'))
        else:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'wall.png'))