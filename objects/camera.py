#todo write camera component class
from scripts.constants import CELL_SIZE
import pygame

class Camera:
    """Used for display the part of the game surface centered on a particular entity such as the player"""
    width = 15
    height = 15
    
    def __init__(self, owner):
        self.owner = owner
        self.pixel_width = self.width * CELL_SIZE
        self.pixel_height = self.height * CELL_SIZE
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
        
        
        
        
    