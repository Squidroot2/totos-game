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
    floor1 = Floor(MAP_WIDTH, MAP_HEIGHT)
    player = entities.Player(0,0)
    floor1.entities.append(player)

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_KP8:
                    player.move(floor1, 0,-1)
                if event.key == K_DOWN or event.key == K_KP2:
                    player.move(floor1, 0, 1)
                if event.key == K_LEFT or event.key == K_KP4:
                    player.move(floor1, -1, 0)
                if event.key == K_RIGHT or event.key == K_KP6:
                    player.move(floor1, 1, 0)
                if event.key == K_KP7:
                    player.move(floor1,-1,-1)
                if event.key == K_KP9:
                    player.move(floor1,1,-1)
                if event.key == K_KP1:
                    player.move(floor1,-1,1)
                if event.key == K_KP3:
                    player.move(floor1,1,1)

                for enemy in floor1.enemies:
                    enemy.randomMove(floor1)

        floor1.draw(SCREEN)
        player.draw(SCREEN)
        for enemy in floor1.enemies:
            enemy.draw(SCREEN)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def terminateGame():
    '''Quits the game'''
    pygame.quit()
    sys.exit()

class Floor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = tcod.map.Map(width,height)
        self.tile_map = [[Tile(x, y, self.map) for y in range(height)] for x in range(width)]

        # primitive random generation
        for xtile in range(self.width):
            for ytile in range(self.height):
                roll_block = random.randint(0,9)
                if roll_block != 0:
                    self.map.walkable[ytile][xtile] = True
                    self.map.transparent[ytile][xtile] = True
        self.updateTiles()
        self.enemies = self.generateEnemies(3)
        self.entities = []
        self.entities += self.enemies


    def generateEnemies(self, number_of_enemies):
        enemy_list = []
        for enemy in range(number_of_enemies):
            x = random.randint(0, self.width -1)
            y = random.randint(0, self.height -1)
            new_enemy = entities.Enemy(x, y)
            enemy_list.append(new_enemy)
        return enemy_list


    def draw(self, surface):
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].draw(surface)

    def updateTiles(self):
        for xtile in range(self.width):
            for ytile in range(self.height):
                self.tile_map[xtile][ytile].update(self.map)

class Tile:
    def __init__(self, x, y, map):
        # Row Major Order
        self.walkable = map.walkable[y][x]
        self.transparent = map.transparent[y][x]
        self.x = x
        self.y = y

    def update(self, map):
        self.walkable = map.walkable[self.y][self.x]
        self.transparent = map.transparent[self.y][self.x]

    def draw(self, surface):
        if self.walkable and self.transparent:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'white-tile.png'))
        else:
            self.image = pygame.image.load(os.path.join('images', 'tiles', 'black-tile.png'))
        surface.blit(self.image, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT))

if __name__ == '__main__':
    initializePygame()
    runGameLoop()
    terminateGame()
