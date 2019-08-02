"""Testing the performance of blits vs  mutlitiple blit calls

The results seem to indicate there is no significant performance difference
"""
import pygame
import time
import sys
import pickle
from pygame.constants import QUIT, HWSURFACE


draw_over = 1
USE_BLITS = False

# Run Time in Seconds
RUN_TIME = 60

def main():

    window, fps_clock = initializePygame()
    floor = Floor()
    
    window_rect = window.get_rect()
    
    font = pygame.font.Font('freesansbold.ttf', 30)
    
    red = (255,0,0)
    
    fps_list = []
    
    if USE_BLITS:
        draw_function = floor.drawBlits
        file_name = 'blits'
    
    else:
        draw_function = floor.draw
        file_name = 'blit'
    
    
    run_test = True
    start = time.process_time()
    while run_test:
        for event in pygame.event.get(QUIT):
            run_test = False
            
        
        draw_function(window)
        
        #drawFPS(window, fps_clock, window_rect.center, font, color=red)
        
        if time.process_time() - start > RUN_TIME:
            run_test = False
        
        pygame.display.flip()
        fps_clock.tick()
        fps_list.append(fps_clock.get_fps())
    
    
    # Dump Results
    with open(str(file_name) +'.pickle', 'wb') as file:
        pickle.dump(fps_list, file)
    
def initializePygame():
    pygame.init()
    fps_clock = pygame.time.Clock()
    win_width= 1280
    win_height = 720
    window = pygame.display.set_mode((win_width, win_height))
    return window, fps_clock

def drawFPS(window, fps_clock, center, font, color):
    fps = int(fps_clock.get_fps())
    
    fps_surf = font.render(str(fps), False, color)
    fps_rect = fps_surf.get_rect()
    fps_rect.center = center
    
    window.blit(fps_surf, fps_rect)

class Floor:
    width = 40
    height = 30
    
    def __init__(self):
        self.tile_map = [[Tile(x, y) for y in range(self.height)] for x in range(self.width)]

    def draw(self, surface):
        """Uses multiple blit calls"""
        
        for i in range(draw_over):
            for x in range(self.width):
                for y in range(self.height):
                    self.tile_map[x][y].draw(surface)
        
    def drawBlits(self, surface):
        """Uses a single blits call"""
        blit_list = list()
        
        for i in range(draw_over):
            for x in range(self.width):
                for y in range(self.height):
                    blit_list.append(self.tile_map[x][y].getDraw())
        
        surface.blits(blit_list)
        
class Tile:
    cell_size = 32
    image = pygame.image.load('wall.png')
    
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        
        self.pixel_x = self.x*self.cell_size
        self.pixel_y = self.y*self.cell_size
    
    def draw(self, surface):
        surface.blit(self.image, (self.pixel_x, self.pixel_y))
    
    def getDraw(self):
        return self.image, (self.pixel_x, self.pixel_y)
        

if __name__ == '__main__':
    main()
    
        