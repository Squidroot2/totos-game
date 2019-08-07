"""Projectile class"""
from source.assets import Images
from source.constants import CELL_SIZE


# todo write projectile class
class Projectile:
    image_dir = 'Projectiles'
    frames_on_screen = 100

    def __init__(self, id, location, source, destination):
        """Takes in source in destination as tuples that indicate coords on tile_map"""
        self.pixelx = source[0] * CELL_SIZE + (CELL_SIZE/2)
        self.pixely = source[1] * CELL_SIZE + (CELL_SIZE/2)

        self.dest_pixelx = destination[0] * CELL_SIZE + (CELL_SIZE/2)
        self.dest_pixely = destination[1] * CELL_SIZE + (CELL_SIZE/2)

        self.image = Images.getImage(self.image_dir, id)

        self.x_step = self.dest_pixelx - self.pixelx


    def draw(self, surface):
        pass


    def move(self):
        self.pixely