#Python modules

#third party modules
from pygame.constants import *

#my modules
from scripts.constants import *
from scripts.characters import *
from scripts.floors import Floor


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
    player = Player(floor1,0,0,components={'Inventory': []})
    floor1.entities.append(player)

    #game loop
    while run_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False
                break

            elif event.type == KEYDOWN:
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

                for entity in floor1.entities:
                    if entity.ai:
                        entity.ai.takeTurn()

        floor1.draw(SCREEN)
        player.draw(SCREEN)
        for entity in player.location.entities:
            entity.draw(SCREEN)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    initializePygame()
    runGameLoop()
