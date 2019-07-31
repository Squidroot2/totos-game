"""Contains the objects reprenting the Floor and the Tiles on items

Classes:
    Floor
    Tile
"""
# Standard Library
import os
import random
import queue
# Third Party
import pygame
import tcod
# My Modules
from source.entities import Portal
from source.entities import Character
from source.constants import CELL_SIZE, FLOOR_HEIGHT, FLOOR_WIDTH, COLORS
from source.assets import Images



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
        self.path_finder = tcod.path.AStar(self.map, diagonal=1)
        self.number = floor_number

        # Initialize empty variables
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
        """Uses the properties of the given node to dig out a room. Appends the room to the instance's list of rooms

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
                direction = "down"

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
        chance_per_room = .3

        for room in self.rooms:
            if room is self.landing_room:
                continue
            roll = random.random()
            if roll < chance_per_room:
                x = random.randrange(room['x'], room['x']+room['w'])
                y = random.randrange(room['y'], room['y']+room['h'])
                Character("BLOB_1", self, x, y)

    def updateTiles(self):
        """Runs the update method on every tile in the tile_map"""
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].update(self.map)

    def draw(self, surface, camera):
        """Draws all of the tiles in the tile map at the appropriate location

        Parameters:
            surface : pygame.Surface : surface to draw to
            camera : source.components.Camera :
        """

        area = camera.getTileRect()
        for xtile in range(area.left, area.right):
            # ignore if out of range
            if xtile >= len(self.tile_map) or xtile < 0:
                continue
            for ytile in range(area.top, area.bottom):
                # ignore if out of range
                if ytile >= len(self.tile_map[xtile]) or ytile < 0:
                    continue
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

    def drawFog(self, surface, camera):
        """Grays out areas that have been discovered but are no longer in FOV

        Parameters:
            surface : pygame.Surface : surface to draw to
            camera : source.components.Camera
        """
        area = camera.getTileRect()

        for x in range(area.left, area.right):
            if x >= len(self.tile_map) or x < 0:
                continue
            for y in range(area.top, area.bottom):
                if y >= len(self.tile_map[x] or y < 0):
                    continue
                if self.tile_map[x][y].discovered and not self.map.fov[y][x]:
                    self.tile_map[x][y].drawFog(surface)

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

    @staticmethod
    def generateDungeonProcess(floors_to_make, floors_made):
        """To be run from a Process. Saves the floors in floors_made
        
        Currently unused"""
        while True:
            try:
                number = floors_to_make.get_nowait()
            except queue.Empty:
                return
            else:
                floors_made.put(Floor(number))
                print("Finished floor %d" % number)


class Tile:
    CELL_SIZE = CELL_SIZE
    image_dir = "Tiles"

    def __init__(self, map, x, y):
        # Row Major Order
        self.walkable = map.walkable[y][x]
        self.transparent = map.transparent[y][x]
        self.x = x
        self.y = y
        self.discovered = False
        self.pixel_x = self.x*self.CELL_SIZE
        self.pixel_y = self.y*self.CELL_SIZE
        self.image_name = None
        self.image = None

    def draw(self, surface):
        """Blits the tile to the screen if it has been discovered"""

        if self.discovered:
            surface.blit(self.image, (self.pixel_x, self.pixel_y))

    def update(self, map):
        """Loads the image for each image depending on the values in the walkable and transparent array"""
        self.walkable = map.walkable[self.y][self.x]
        self.transparent = map.transparent[self.y][self.x]
        if self.walkable and self.transparent:
            self.image_name = 'white-tile'
            
        else:
            self.image_name = 'wall'
        
        self.image = Images.getImage(self.image_dir, self.image_name)

    def drawFog(self, surface):
        """Covers the tile in a translucent gray surface"""

        surf = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE))
        surf.set_alpha(128)
        surf.fill(COLORS['DARK GRAY'])
        surface.blit(surf, (self.pixel_x, self.pixel_y))

    def getRect(self):
        """Returns a rect representing the area and location of the tile"""
        left = self.x*self.CELL_SIZE
        top = self.y*self.CELL_SIZE
        width = self.CELL_SIZE
        height = self.CELL_SIZE
        return pygame.Rect(left, top, width, height)
