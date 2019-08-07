"""Contains the objects representing the Floor and the Tiles on items

Classes:
    Floor
    Tile
"""
# Standard Library
import random
import queue
# Third Party
import pygame
import tcod
# My Modules
from source.entities import Portal, Item, Character
from source.constants import CELL_SIZE, FLOOR_HEIGHT, FLOOR_WIDTH, COLORS
from source.assets import Images, Data


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

        # Initialize empty variables
        self.entities = []
        self.sort_entities = False
        self.projectiles = []
        self.rooms = []
        self.portals = {'up': None, 'down': None}
        self.landing_room = None
        
        # Random Generation of Floor
        self.generateLayout()
        self.updateTiles()
        self.generatePortals()
        self.generateItems()
        self.generateEnemies()

        # Get pathfinder, diagonal is just slightly higher than 1 to make paths a little straighter
        self.path_finder = tcod.path.AStar(self.map, diagonal=1.01)

    def generateLayout(self):
        """Uses Binary Space Partition to generate the layout of the dungeon"""
        bsp = tcod.bsp.BSP(0, 0, self.width-1, self.height-1)
        bsp.split_recursive(depth=5, min_width=3, min_height=3, max_horizontal_ratio=2, max_vertical_ratio=2)
        for node in bsp.pre_order():
            if node.children:
                self.makeHallway(node)

            else:
                self.makeRoom(node)

    def makeHallway(self, node):
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

    def makeRoom(self, node):
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

        self.rooms.append({"x": x, "y": y, "w": width, "h": height})

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

            # noinspection PyTypeChecker
            self.portals[direction] = Portal(self, x, y, direction)
            if direction == "up":
                self.landing_room = room

    def generateEnemies(self):
        """Goes trhough each room and rolls to determine if an enemy is going to be in that room. Then it decides which enemy based on the leveled list """
        chance_per_room = .5
        leveled_list = Data.getLeveledList("ENEMIES", self.number)

        for room in self.rooms:
            if room is self.landing_room:
                continue
            roll = random.random()
            if roll < chance_per_room:
                # Find location in room
                x = random.randrange(room['x'], room['x']+room['w'])
                y = random.randrange(room['y'], room['y']+room['h'])

                # Get random char_id from leveled list
                char_id = random.choices(list(leveled_list.keys()), list(leveled_list.values()))[0]

                # Create Character
                Character(char_id, self, x, y)
    
    def generateItems(self):
        """Based on the level list, determines items that show up"""
        # Uses a random function to determine if the number of items on the floor
        num_of_items = round(random.triangular(low=1,high=6,mode=5))
        
        # Get leveled list
        leveled_list = Data.getLeveledList("ITEMS", self.number)
        
        # For each item in the number of items...
        for i in range(num_of_items):
        
            # Get the location for the item
            room = random.choice(self.rooms)
            x = random.randrange(room['x'], room['x']+room['w'])
            y = random.randrange(room['y'], room['y']+room['h'])
            
            # Gets the item from the leveled_list
            item_id = random.choices(list(leveled_list.keys()), list(leveled_list.values()))[0]
            
            # Create the item
            Item.createItem(item_id, self, x, y)
        
    def updateTiles(self):
        """Runs the update method on every tile in the tile_map"""
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].update(self.map)

    def draw(self, surface, camera):
        """Draws all of the tiles, entities, and the finally the fog

        Parameters:
            surface : pygame.Surface : surface to draw to
            camera : source.components.Camera 
        """

        area = camera.getTileRect()

        # Draw the tile map
        for xtile in range(area.left, area.right):
            # ignore x out of range
            if xtile >= len(self.tile_map) or xtile < 0: continue
            
            for ytile in range(area.top, area.bottom):
                # ignore y out of range
                if ytile >= len(self.tile_map[xtile]) or ytile < 0: continue
                self.tile_map[xtile][ytile].draw(surface)

        # Sort entities if needed
        if self.sort_entities:
            self.entities.sort(key=lambda entity: entity.draw_order)
            self.sort_entities = False
           
        # Draw the entities in the map
        for entity in self.entities:
            if self.map.fov[entity.y][entity.x]:
                # If the entity is in fov, mark as discovered, update last known coordinates, and draw
                entity.discovered = True
                entity.last_known_x = entity.x
                entity.last_known_y = entity.y
                entity.draw(surface)
            elif entity.discovered and not self.map.fov[entity.last_known_y][entity.last_known_x]:
                # If the entity is not in fov but is discovered, draw at last known coordinates...
                # unless the last known coordinates are in FOV
                entity.drawAtLastKnown(surface)
        
        # Draw the fog over the area not in the fov
        for x in range(area.left, area.right):
            # Ignore x out of range
            if x >= len(self.tile_map) or x < 0: continue
            
            for y in range(area.top, area.bottom):
                # Ignore y out of range
                if y >= len(self.tile_map[x] or y < 0): continue
                
                # Draw fog if discovered but no longer in fov
                if self.tile_map[x][y].discovered and not self.map.fov[y][x]:
                    self.tile_map[x][y].drawFog(surface)
        
        for projectile in self.projectiles:
            projectile.drawNextStep(surface)
        
            
            

    def addEntity(self, entity):
        """Adds an entity to the entities list attribute

        Parameters:
            entity : Entity
        """
        self.entities.append(entity)
        self.sort_entities = True
        
    def removeEntity(self, entity):
        """Removes an entity from the entities list attribute"""
        self.entities.remove(entity)
    
    def addProjectile(self, projectile):
        """Adds a projectile to the projectiles list"""
        self.projectiles.append(projectile)
    
    def removeProjectile(self, projetile):
        """Removes the projectile from the projectiles list"""
        self.projectiles.remove(projectile)

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

    def __init__(self, tcod_map, x, y):
        # Row Major Order
        self.walkable = tcod_map.walkable[y][x]
        self.transparent = tcod_map.transparent[y][x]
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

    def getDraw(self):
        """Returns a tuple with image and location. Perhaps used for mass blitting"""
        return self.image, (self.pixel_x, self.pixel_y)

    def update(self, tcod_map):
        """Loads the image for each image depending on the values in the walkable and transparent array"""
        self.walkable = tcod_map.walkable[self.y][self.x]
        self.transparent = tcod_map.transparent[self.y][self.x]
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
    
    def addSplatter(self):
        """Copies the images and adds a blood splatter to it"""
        self.image = self.image.copy()
        splatter = Images.getRandomSplatter()
        self.image.blit(splatter, (0,0))
