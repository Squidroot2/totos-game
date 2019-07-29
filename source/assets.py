"""Module which will hold a struct-like class which wiil load all assets to one place"""
# Standard Library
import os
# Third Party
import pygame
# My Modules
from source.utilities import loadJson

def loadAssets()
    """Runs the load method on all classes"""
    Assets.load()
    Data.load()



# todo have tiles and entities pull from the loaded assets
# todo rename this to Images
class Assets:
    # Image Folders
    images_folder = 'images'
    character_images = os.path.join(images_folder, 'characters')
    other_images = os.path.join(images_folder, 'other')
    tile_images = os.path.join(images_folder, 'tiles')
    
    # Missing Image
    missing_image_path = os.path.join(images_folder, 'unknown.png')
    missing_image = None
    
    # Image Paths
    image_paths = { 'Characters': {
                        'blob': os.path.join(character_images,'blob.png'),
                        'blue_slinger': os.path.join(character_images,'blue_slinger.png'),
                        'player': os.path.join(character_images,'player.png'),
                        'weirdmonk': os.path.join(character_images,'weirdmonk.png')
                    },
                    'Other': {

                        'down_portal': os.path.join(other_images, 'down_portal.png'),
                        'up_portal': os.path.join(other_images, 'up_portal.png'),
                        'headstone': os.path.join(other_images, 'headstone.png'),
                        'target': os.path.join(other_images, 'target.png'),
                    },
                    'Tiles': {
                        'wall': os.path.join(tile_images, 'wall.png'),
                        'white-tile': os.path.join(tile_images, 'white-tile.png')
                    }
    }
    
    # Dictionary comprehension doesn't work inside classes for some silly reason
    # images = {folder: {image: None for image in image_paths[folder]} for folder in image_paths}
    
    # Creates an 'images' dictionary that is the same as the same structure as image_paths
    images = dict()
    for folder in image_paths:
        images[folder] = dict()
        for image in image_paths[folder]:
            images[folder][image] = None
    
    
    @classmethod
    def load(cls):
        """Loads the images into the class dictionary
        
        Requires pygame to be initialized and video mode to be set
        """
        for folder in cls.image_paths:
            for image in cls.image_paths[folder]:
                cls.images[folder][image] = pygame.image.load(cls.image_paths[folder][image]).convert_alpha()
        cls.missing_image = pygame.image.load(cls.missing_image_path)
    
    @classmethod
    def getImage(cls, directory, image):
        """Returns the correct image unless it cannot be found in which case it returns the missing_image surface
        
        Parameters:
            directory : string
            image : string
        
        Returns: pygame.Surface
        """
        try:
            return cls.images[directory][image]
        except KeyError:
            return cls.missing_image

class Data:
    """Contains data pulled from json files"""
    data_folder = 'data'
    
    json_files = {'Characters': os.path.join(data_folder, 'characters.json'),
                  'Items': os.path.join(data_folder, 'items.json')}
    
    data = {file: None for file in json_file}
        
        
    
    def load(cls):
        """Loads the data from the json files"""
        for file in cls.json_files:
            cls.data[file] = loadJson(cls.json_files[file])
    
    
    def getCharacter(cls, id):
        """Returns the data for a charcter with a given id"""
        return cls.data['Characters'][id]
    
    
    def getItem(cls, category, id):
        """Returns the data for an item for given category and id"""
        return cls.data['Items'][category][id]
        
