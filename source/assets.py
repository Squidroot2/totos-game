"""Module which will hold struct-like classes which wiil load all assets into memory before the game starts

Functions:
    loadAssets() : Runs the load method on all classes

Classes:
    Images : Contains the png files for use throughout the game
    Data : Contains data pulled from json files
"""
# Standard Library
import os
import random
# Third Party
import pygame
from pygame.font import Font
# My Modules
from source.utilities import loadJson


def loadAssets():
    """Runs the load method on all classes"""
    Images.load()
    Data.load()
    #Fonts.create()


class Images:
    """Contains the png files for use throughout the game"""
    # Image Folders
    main_folder = 'images'
    character_images = os.path.join(main_folder, 'characters')
    other_images = os.path.join(main_folder, 'other')
    tile_images = os.path.join(main_folder, 'tiles')
    item_images = os.path.join(main_folder, 'items')
    bg_images = os.path.join(main_folder, 'backgrounds')
    splatter_images = os.path.join(main_folder, 'splatters')
    proj_images = os.path.join(main_folder, 'projectiles')
    
    # Missing Image
    missing_image_path = os.path.join(main_folder, 'unknown.png')
    missing_image = None
    
    # Image Paths
    image_paths = { 'Characters': {
                        'blob': os.path.join(character_images,'blob.png'),
                        'blue_slinger': os.path.join(character_images,'blue_slinger.png'),
                        'player': os.path.join(character_images,'player.png'),
                        'weirdmunk': os.path.join(character_images,'weirdmunk.png'),
                        'geomefox': os.path.join(character_images, 'geomefox.png'),
                        'aviboy': os.path.join(character_images, 'aviboy.png')
                    },
                    'Other': {
                        'down_portal': os.path.join(other_images, 'down_portal.png'),
                        'up_portal': os.path.join(other_images, 'up_portal.png'),
                        'headstone': os.path.join(other_images, 'headstone.png'),
                        'target': os.path.join(other_images, 'target.png'),
                        'force_field': os.path.join(other_images, 'forcefield.png')
                    },
                    'Tiles': {
                        'wall': os.path.join(tile_images, 'wall.png'),
                        'white-tile': os.path.join(tile_images, 'white-tile.png')
                    },
                    'Items': {
                        'pistol1': os.path.join(item_images, 'pistol1.png'),
                        'dagger1': os.path.join(item_images, 'dagger1.png'),
                        'battery_tiny': os.path.join(item_images, 'battery_tiny.png'),
                        'armor1': os.path.join(item_images, 'armor_1.png')
                    },
                    'Backgrounds': {
                        'title': os.path.join(bg_images, 'title_screen.png'),
                        'starry': os.path.join(bg_images, 'starry_bg.png')
                    },
                    'Splatters' : {},
                    'Projectiles' : {}
    }

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
    
    @classmethod
    def getRandomSplatter(cls):
        """Returns a random image from the splatter directory"""
        splatter = random.choice(cls.images['Splatters'])
        return cls.images['Splatters'][splatter]
        
        


class Data:
    """Contains data pulled from json files"""
    data_folder = 'data'
    
    json_files = {'Characters': os.path.join(data_folder, 'characters.json'),
                  'Items': os.path.join(data_folder, 'items.json'),
                  'Leveled_Lists': os.path.join(data_folder, 'leveled_lists.json'),
                  'Inventories': os.path.join(data_folder, 'inventories.json')}
    
    data = dict()
    for file in json_files:
        data[file] = None

    @classmethod
    def load(cls):
        """Loads the data from the json files"""
        for file in cls.json_files:
            cls.data[file] = loadJson(cls.json_files[file])
    
    @classmethod
    def getCharacter(cls, identifier):
        """Returns the data for a charcter with a given id"""
        return cls.data['Characters'][identifier]
    
    @classmethod
    def getItem(cls, category, identifier):
        """Returns the data for an item for given category and id"""
        return cls.data['Items'][category][identifier]

    @classmethod
    def getLeveledList(cls, category, level):
        """Category is characters or items, level is an int. Returns a dict"""
        levels = cls.data['Leveled_Lists'][category]

        # Try to return the specified level but if not found, return the level present closest without going over
        while True:
            try:
                return levels['LEVEL_'+str(level)]
            except KeyError:
                level -= 1

    @classmethod
    def getInventory(cls, type, level):
        """Gets a leveled invenotry from the invenotry json

        Parameters:
            type : string
            level : int

        Returns : dict
        """
        levels = cls.data['Inventories'][type]

        # Try to return the specified level but if not found, return the level present closest without going over
        while True:
            try:
                return levels['LEVEL_'+str(level)]
            except KeyError:
                level -= 1

    @classmethod
    def getPlayerInventory(cls, background):
        return cls.data['Inventories']['PLAYER'][background]


#todo use Fonts Class to create Fonts
class Fonts:
    main_folder = 'fonts'
    
    # Font types
    unispace_folder = os.path.join(main_folder, 'unispace')
    
    files = {'default': 'freesansbold.ttf',
             'unispace_rg': os.path.join(unispace_folder, 'unispace_rg.ttf')}
    
    fonts = dict()
             
    @classmethod
    def create(cls):
        cls.fonts = {
                'Title':        Font(cls.files['default'], 70),
                'Main':         Font(cls.files['default'], 28),
                'Submain':      Font(cls.files['default'], 20),
                'Info_Header':  Font(cls.files['unispace_rg'], 16),
                'Info':         Font(cls.files['unispace_rg'], 14),
                'Info_S':       Font(cls.files['unispace_rg'],12),
                'Log':          Font(cls.files['default'],12)}

    
    
    