#third party modules
import pygame, tcod, sys, os
from pygame.constants import *

#my modules
from scripts.constants import *
from scripts.entities import Character

def initializePygame():
    '''Initializes the pygame modules and creates the global variables SCREEN and FPS_CLOCK'''

    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def runGameLoop():
    '''runs the main game loop as long as the run_game boolean is true'''
    player = Character(0,0)

    run_game = True
    map1 = Map(30,30)
    map1.draw(SCREEN)
    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    pass
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_map = [[Tile(False, x, y) for y in range(height)] for x in range(width)]

    def draw(self, surface):
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].draw(surface)


class Tile:
    def __init__(self, block_path, x, y):
        self.block_path = block_path
        self.x = x
        self.y = y
        if block_path:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'black-tile.png'))
        else:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'white-tile.png'))

    def draw(self, surface):
        surface.blit(self.image, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT))

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
    terminateGame()
