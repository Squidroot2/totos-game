"""Module which will hold a struct-liek class which wiil load all assets to one place"""
import os

import pygame

# # Image Folders
# images_folder = 'images'
# character_images = os.path.join(images_folder, 'characters')
# other_images = os.path.join(images_folder, 'other')
# tile_images = os.path.join(images_folder, 'tiles')
#
# image_paths = {'Characters': {
#     'blob': os.path.join(character_images, 'blob.png'),
#     'blue_slinger': os.path.join(character_images, 'blue_slinger.png'),
#     'player': os.path.join(character_images, 'player.png'),
#     'weirdmonk': os.path.join(character_images, 'weirdmonk.png')
# },
#     'Other': {
#
#         'down_portal': os.path.join(other_images, 'down_portal.png'),
#         'up_portal': os.path.join(other_images, 'up_portal.png'),
#         'headstone': os.path.join(other_images, 'headstone.png'),
#         'target': os.path.join(other_images, 'target.png'),
#     },
#     'Tiles': {
#         'wall': os.path.join(tile_images, 'wall.png'),
#         'white-tile': os.path.join(tile_images, 'white-tile.png')
#     }
# }
# # Creates an empty dictionary based on the image_paths dictionary. Images will be loaded into this
# images = {folder: {image: None for image in image_paths[folder]} for folder in image_paths}


class Assets:
    # Image Folders
    images_folder = 'images'
    character_images = os.path.join(images_folder, 'characters')
    other_images = os.path.join(images_folder, 'other')
    tile_images = os.path.join(images_folder, 'tiles')

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
    images = dict()
    for folder in image_paths:
        images[folder] = dict()
        for image in image_paths[folder]:
            images[folder][image] = None
   # images = {folder: {image: None for image in image_paths[folder]} for folder in image_paths}

    @classmethod
    def loadImages(cls):
        for folder in cls.image_paths:
            for image in folder:
                cls.images[folder][image] = pygame.image.load(cls.image_paths[folder][image])

