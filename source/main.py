""" The main module for the grim ranger game

Functions:
    main() : main function of the program
    initializePygame: Initializes the pygame module and returns pygame objects
    setupGame(window, fps_clock) : Gets information from the user then creaetes player and dungeon and puts them in a Game object
"""
import pygame
from source.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from source.entities import Player
from source.game import Game
from source.screens import mainGameScreen, titleScreen, playerCreateScreen, gameOverScreen, generateDungeonScreen, mainMenuScreen
from source.assets import loadAssets

def main():
    """The main function of the program
    
    Initializes pygame. Setups Game, Runs the game, finally presents game over screen before repeating loop"""
    window, fps_clock = initializePygame()
    loadAssets()
    titleScreen(window, fps_clock)
    mainMenuScreen(window, fps_clock)

    while True:
        game = setupGame(window, fps_clock)
        mainGameScreen(window,fps_clock,game)
        gameOverScreen(window, fps_clock)

def initializePygame():
    """Initializes the pygame modules and returns SCREEN and FPS_CLOCK
    
    Returns:
        window : pygame.Surface
        fps_clock : pygame.Clock
    """

    pygame.init()
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return window, fps_clock


def setupGame(window, fps_clock):
    """Runs the titleScreen and the playerCreateScreen to get information from user. Then, creates player and dungeon and puts them in a game object
    
    Parameters:
        window : pygame.Surface
        fps_clock : pygame.Clock
    
    Returns:
        game : source.game.Game
    
    Calls:
        source.assets
            loadAssets() 
        source.screens
            titleScreen(window, fps_clock)
            playerCreateScreen(window, fps_clock)
            generateDungeonScreen(window, fps_clock)
        source.entities
            Player(name, background, location, x, y)
        source.game
            Game(dungeon, player)
    """

    name, background = playerCreateScreen(window, fps_clock)

    # Shows loading screen for generating dungeon
    dungeon = generateDungeonScreen(window)

    # Player starts on the first floor at the location of the up portal
    player_start_x = dungeon[0].portals['up'].x
    player_start_y = dungeon[0].portals['up'].y

    # Generates player
    player = Player(name, background, dungeon[0], player_start_x, player_start_y)

    # Creates game from player and dungeon
    game = Game(dungeon, player)

    return game