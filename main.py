#Python modules
import sys, os, random

#third party modules
import pygame, tcod
from pygame.constants import *

#my modules
from scripts.constants import *
from scripts import entities

def initializePygame():
    '''Initializes the pygame modules and creates the global variables SCREEN and FPS_CLOCK'''

    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def runGameLoop():
    '''runs the main game loop as long as the run_game boolean is true'''

    run_game = True
    map1 = Map(MAP_WIDTH,MAP_HEIGHT)
    player = entities.Player(0,0,map1)
    map1.entities.append(player)

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                break

            if event.type == KEYDOWN:
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

                for entity in map1.entities:
                    if entity.ai:
                        entity.ai.takeTurn()

        map1.draw(SCREEN)
        player.draw(SCREEN)
        for entity in player.map.entities:
            entity.draw(SCREEN)
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

        # primitive random generation
        for xtile in range(self.width):
            for ytile in range(self.height):
                roll_block = random.randint(0,9)
                if roll_block == 0:
                    self.tile_map[xtile][ytile].block_path = True
        enemies = self.generateEnemies(3)
        self.entities = []
        self.entities += enemies


    def generateEnemies(self, number_of_enemies):
        enemy_list = []
        for enemy in range(number_of_enemies):
            x = random.randint(0, self.width -1)
            y = random.randint(0, self.height -1)
            new_enemy = entities.Enemy(x, y, self, ['AI'])
            enemy_list.append(new_enemy)
        return enemy_list


    def draw(self, surface):
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].draw(surface)


class Tile:
    def __init__(self, block_path, x, y):
        self.block_path = block_path
        self.x = x
        self.y = y


    def draw(self, surface):
        if self.block_path:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'black-tile.png'))
        else:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'white-tile.png'))
        surface.blit(self.image, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT))

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
