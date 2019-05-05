#third party modules
import pygame, tcod, sys
from pygame.constants import *

#my modules
from scripts.constants import *
from scripts.actors import Character

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


def createMap():
    game_map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

class Tile:
    def __init__(self, block_path):
        self.block_path = block_path

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
    terminateGame()
