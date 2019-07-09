#Python modules
import sys, os, random

#third party modules
import pygame
import tcod
from pygame.constants import *

#my modules
from scripts.constants import *
from scripts.characters import *

def initializePygame():
    '''Initializes the pygame modules and creates the global variables SCREEN and FPS_CLOCK'''

    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def runGameLoop():
    '''runs the main game loop as long as the run_game boolean is true'''
    run_game = True
    floor1 = Floor(MAP_WIDTH, MAP_HEIGHT)
    player = Player(0,0,floor1,components={'Inventory': []})
    floor1.entities.append(player)

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_KP8:
                    player.move(0, -1)
                elif event.key == K_DOWN or event.key == K_KP2:
                    player.move(0, 1)
                elif event.key == K_LEFT or event.key == K_KP4:
                    player.move(-1, 0)
                elif event.key == K_RIGHT or event.key == K_KP6:
                    player.move(1, 0)
                elif event.key == K_KP7:
                    player.move(-1, -1)
                elif event.key == K_KP9:
                    player.move(1, -1)
                elif event.key == K_KP1:
                    player.move(-1, 1)
                elif event.key == K_KP3:
                    player.move(1, 1)

                for entity in floor1.entities:
                    if entity.ai:
                        entity.ai.takeTurn()

        floor1.draw(SCREEN)
        player.draw(SCREEN)
        for entity in player.location.entities:
            entity.draw(SCREEN)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()

# todo use the tcod.Map object

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
            Enemy(x, y, self, ['AI'])

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

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
