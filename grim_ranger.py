import pygame
from scripts.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from objects.player import Player
from objects.floors import Floor
from objects.game import Game
from scripts.screens import mainGameScreen, titleScreen, playerCreateScreen, gameOverScreen

def main():
    window, fps_clock = initializePygame()
    while True:
        game = setupGame(window, fps_clock)
        mainGameScreen(window,fps_clock,game)
        gameOverScreen(window, fps_clock)

def initializePygame():
    """Initializes the pygame modules and returns SCREEN and FPS_CLOCK"""

    pygame.init()
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return window, fps_clock


# Todo make this a static method of Game
def setupGame(window, fps_clock):

    titleScreen(window, fps_clock)
    name = playerCreateScreen(window, fps_clock)

    # Generate a dungeon with a specified number of floors
    dungeon = Floor.generateDungeon(num_of_floors=5)

    # Player starts on the first floor at th location of the up portal
    player_start_x = dungeon[0].portals['up'].x
    player_start_y = dungeon[0].portals['up'].y

    # Generates player
    player = Player(name,"Officer",dungeon[0],player_start_x,player_start_y)

    # Creates game from player and dungeon
    game = Game(dungeon,player)

    return game


if __name__ == '__main__':
    main()