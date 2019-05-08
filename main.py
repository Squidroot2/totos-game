#third party modules
import pygame, tcod, sys
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

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

            if event.type == KEYDOWN:
                if event.key == K_UP:

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()


class Map:
    def __init__(self, width, height):
        game_map = [[Tile(False) for y in range(height)] for x in range(width)]


class Tile:
    def __init__(self, block_path):
        self.block_path = block_path
    def draw(self, surface):
        surface.blit(self.image, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT))

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
    terminateGame()
