import os

import numpy
import pygame

from objects.camera import Camera
from objects.characters import Character
from objects.items import Weapon, Armor, Generator, Battery


class Player(Character):
    image = pygame.image.load(os.path.join('images', 'characters', 'player.png'))

    def __init__(self, name, background, floor, x, y):
        """Extends the Character init method

        Parameters:
            name : string
                name of the player
            background : string
                background of the player which determines the starting items
                Valid Attributes are ['Officer','Marksman','Agent','Pointman','Gladiator']
            floor : Floor
                the starting location of the player
            x : int
                starting x position on the floor
            y : int
                starting y position on the floor
        """

        super().__init__("PLAYER", floor, x, y, inventory=[], is_player=True)

        # Overrides the name set by the Character init method
        self.name = name

        # Stores the background
        assert background in ("Officer", "Marksman", "Agent", "Pointman", "Gladiator")
        self.background = background

        self.setStartingInventory()

        # Player-Specific Component
        self.camera = Camera(self)

        # Start with a calculated FOV
        self.calculateFOV()
        self.discoverTiles()

    # todo move inventory stuff to inventory class with ids
    def setStartingInventory(self):

        # Create Initial Items in Inventory
        if self.background == "Officer":
            weapon = Weapon("PISTOL_1", self.inventory)
            armor = Armor("ARMOR_1", self.inventory)
            generator = Generator("QUICK_1", self.inventory)
            Weapon("KNIFE_1", self.inventory)

        elif self.background == "Marksman":
            weapon = Weapon("RIFLE_1", self.inventory)
            armor = Armor("ARMOR_1", self.inventory)
            generator = Generator("RANGER_1", self.inventory)

        elif self.background == "Agent":
            weapon = Weapon("PDW_1", self.inventory)
            armor = Armor("ARMOR_1", self.inventory)
            generator = Generator("FEEDER_1", self.inventory)

        elif self.background == "Pointman":
            weapon = Weapon("CANNON_1", self.inventory)
            armor = Armor("ARMOR_1", self.inventory)
            generator = Generator("RANGER_1", self.inventory)

        elif self.background == "Gladiator":
            weapon = Weapon("SWORD_1", self.inventory)
            armor = Armor("ARMOR_2", self.inventory)
            generator = Generator("BRAWLER_1", self.inventory)

        # Player starts with 2 batteries
        for i in range(2):
            Battery("BATTERY_1", self.inventory)

        # Equip Items
        weapon.equip()
        armor.equip()
        generator.equip()

        # Shield Starts charged
        generator.rechargeToFull()

    def changeFloors(self, new_floor, direction):
        """Change player's location to a specified floor"""
        assert direction in ("up", "down")
        # If you are going up, you will land on the new floors down portal and vice versa
        if direction == "up":
            portal = "down"
        else:
            portal = "up"

        self.location.removeEntity(self)
        self.x = new_floor.portals[portal].x
        self.y = new_floor.portals[portal].y
        self.location = new_floor
        self.location.addEntity(self)

    def calculateFOV(self):
        self.location.map.compute_fov(self.x, self.y, radius=8)

    def getFOV(self):
        return self.location.map.fov

    def discoverTiles(self):
        fov = numpy.where(self.getFOV())
        for i in range(len(fov[0])):
            self.location.tile_map[(fov[1][i])][(fov[0][i])].discovered = True