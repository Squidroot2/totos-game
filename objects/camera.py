from scripts.constants import CELL_SIZE
import pygame


class Camera:
    """Used for display the part of the game surface centered on a particular entity such as the player
    
    Attrbutes:
        width : int : CLASS; numbers of tiles wide
        height : int : CLASS; numbers of tiles tall
        
    Methods:
        update(self) : Updates the center of the camera based on the location of the owner
        getRect(self) : Returns the rectangle representing the camera in pixel dimensions 
    """
    width = 29
    height = 21
    
    def __init__(self, owner):
        """Camera init function
        
        Parameters:
            owner : Entity
        """
        
        self.owner = owner
        self.pixel_width = self.width * CELL_SIZE
        self.pixel_height = self.height * CELL_SIZE
        self.pixel_center = None
        self.update()
    
    def update(self):
        """Updates the center of the camera based on the location of the owner"""
        self.pixel_center = (self.owner.x*CELL_SIZE+.5*CELL_SIZE, self.owner.y*CELL_SIZE+.5*CELL_SIZE)
    
    def getRect(self):
        """Returns the rectanlge representing the camera in  pixel dimensions 
        
        Returns:
            rect : pygame.Rect
        """
        rect = pygame.Rect(0,0,self.pixel_width,self.pixel_height)
        rect.center = self.pixel_center
        return rect
