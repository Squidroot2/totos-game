"""Projectile class"""
# Standard Library
import math
# Third Party
import pygame
# My Modules
from source.assets import Images
from source.constants import CELL_SIZE


class Projectile:
    image_dir = 'Projectiles'
    frames_on_screen = 8

    def __init__(self, proj_id, location, source, destination, delay):
        """Takes in source in destination as tuples that indicate coords on tile_map"""
        
        # Determines current position
        self.pixelx = source[0] * CELL_SIZE + (CELL_SIZE/2)
        self.pixely = source[1] * CELL_SIZE + (CELL_SIZE/2)
        
        # Determines destination
        self.dest_pixelx = destination[0] * CELL_SIZE + (CELL_SIZE/2)
        self.dest_pixely = destination[1] * CELL_SIZE + (CELL_SIZE/2)

        # Gets the difference between current position and destination
        x_difference = self.dest_pixelx - self.pixelx
        y_difference = self.dest_pixely - self.pixely
        
        # Divides the difference into steps based on the number of frames_on_screen
        self.x_step = x_difference / self.frames_on_screen
        self.y_step = y_difference / self.frames_on_screen
        
        # Adds the Projectile to the location
        self.location = location
        self.location.addProjectile(self)
        
        # Initializes steps taken at 0
        self.steps_taken = 0
        
        # Stores delay
        self.delay = delay
        
        # Determines the angle of the projectile image
        angle = math.degrees(math.atan2(y_difference, x_difference))
        
        # Gets the image and rotates 
        self.image = pygame.transform.rotate(Images.getImage(self.image_dir, proj_id), angle)
        
    def drawNextStep(self, surface):
        
        # If delay, decrement delay
        if self.delay:
            self.delay -= 1
            return
            
        else:
            # Draws the projectile
            surface.blit(self.image, (self.pixelx, self.pixely))
            
            # Moves the projectile
            self.pixely += self.y_step
            self.pixelx += self.x_step
            
            # Increments steps taken
            self.steps_taken += 1
            
            # Determines if projectile has taken enough steps to reach destination
            if self.steps_taken == self.frames_on_screen:
                self.location.removeProjectile(self)
         
        
