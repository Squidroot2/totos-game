#third party modules
import pygame, tcod, sys, os, random
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
    player = entities.Player(0,0)
    enemy_list = generateEnemies(3)

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_KP8:
                    player.move(map1, 0,-1)
                if event.key == K_DOWN or event.key == K_KP2:
                    player.move(map1, 0, 1)
                if event.key == K_LEFT or event.key == K_KP4:
                    player.move(map1, -1, 0)
                if event.key == K_RIGHT or event.key == K_KP6:
                    player.move(map1, 1, 0)
                if event.key == K_KP7:
                    player.move(map1,-1,-1)
                if event.key == K_KP9:
                    player.move(map1,1,-1)
                if event.key == K_KP1:
                    player.move(map1,-1,1)
                if event.key == K_KP3:
                    player.move(map1,1,1)

                for enemy in enemy_list:
                    enemy.randomMove(map1)

        map1.draw(SCREEN)
        player.draw(SCREEN)
        for enemy in enemy_list:
            enemy.draw(SCREEN)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()

def generateEnemies(number_of_enemies):
    enemy_list = []
    for enemy in range(number_of_enemies):
        x = random.randint(0, MAP_WIDTH)
        y = random.randint(0, MAP_HEIGHT)
        new_enemy = entities.Enemy(x,y)
        enemy_list.append(new_enemy)

    return enemy_list


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
    terminateGame()
