#todo write camera component class
from scripts.constants import CELL_SIZE
import pygame

class Camera:
    """Used for display the part of the game surface centered on a particular entity such as the player"""
    TILE_WIDTH = 15
    TILE_HEIGHT = 15
    
    def __init__(self, owner):
        self.owner = owner
        self.rect = self.getRect()
        self.pixel_width = self.TILE_WIDTH*CELL_SIZE
        self.pixel_height = self.TILE_WIDHT*CELL_SIZE
        self.pixel_center = (self.owner.x*CELL_SIZE, self.owner.y*CELL_SIZE)
    
    def update(self):
        """Updates the center of the camera based on the location of the camera"""
        self.pixel_center = (self.owner.x*CELL_SIZE, self.owner.y*CELL_SIZE)
    
    def getRect(self):
        """Retruns the rectanlge in pixel dimensions representing the camera
        
        Returns:
            rect : pygame.Rect
        """
        rect = pygame.Rect(0,0,self.pixel_width,self.pixel_height)
        rect.center = self.pixel_center
        return rect
        
        
        
        
    