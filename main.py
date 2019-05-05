#third party modules
import pygame, tcod, sys
from pygame.constants import *

#my modules
from scripts.constants import *

def initializePygame():
    '''Initializes the pygame modules and creates the global variables SCREEN and FPS_CLOCK'''

    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def runGameLoop():
    '''runs the main game loop as long as the run_game boolean is true'''

    run_game = True

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    initializePygame()
    runGameLoop()
    terminateGame()
