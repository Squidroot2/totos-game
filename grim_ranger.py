#Python modules

#third party modules

#my modules
from scripts.constants import *
from objects.characters import Player
from objects.floors import Floor
from scripts.screens import mainGameScreen, titleScreen, playerCreateScreen

def main():
    window, fps_clock = initializePygame()
    player = setupGame(window, fps_clock)
    mainGameScreen(window,fps_clock,player)

def initializePygame():
    '''Initializes the pygame modules and returns SCREEN and FPS_CLOCK'''

    pygame.init()
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return window, fps_clock

def setupGame(window, fps_clock):

    titleScreen(window, fps_clock)
    name = playerCreateScreen(window, fps_clock)
    floor1 = Floor(MAP_WIDTH, MAP_HEIGHT)
    player = Player(name,"Officer",floor1,0,0)

    return player


if __name__ == '__main__':
    main()