from objects.items import Weapon, Armor, Generator, Battery
from objects.entities import Entity, Corpse
from objects.camera import Camera
from objects.game import Log
from scripts.utilities import getItemById
from scripts import formulas
import pygame, numpy
import os, random

CHARACTER_JSON = os.path.join('data','characters.json')

class Character(Entity):
    """Used for entities which act on the world
    
    Child of Entity
       
    Attributes:
        image_path : string : CLASS; INSTANCE OVERRIDE;
        CELL_SIZE : int : CLASS; INHERITED
        x : int or None : INHERITED
        y : int or None : INHERITED
        location : Floor or Inventory : INHERITED
        obstruct : bool : INHERITED
        image : pygame.Surface : INHERITED
        ai : AI or None : INHERITED
        inventory : Inventory or None : INHERITED
        name : string : The character's name
        level : int
        xp : int : number of xp point the character has
        life : int : how likely a character is going to survive damage to flesh
        base_damage : int : amount of melee damage done with no weapon
        base_defense : int : amount of defense with no armor
        base_attack_rate : int : amount of melee attacks that can be performed
        isDead : bool
    
    Methods:
        loadImage(self) : INHERITED
        draw(self) : INHERITED
        
        
    
    Children:
        Player(Character)"""
    def __init__(self, char_id, floor, x, y, inventory=[]):
        """Extends the entity init function"""

        # Gets the data from the JSON File
        data = getItemById(CHARACTER_JSON, char_id)

        # Copies the info from the data
        self.name = data['name']
        self.level = data['level']
        self.xp = data['xp']
        self.life = data['life']
        self.base_damage = data['damage']
        self.base_defense = data['defense']
        self.base_attack_rate = data['attack_rate']

        # Gets the image
        image_name = data['image']
        self.image_path = os.path.join('images', 'characters', image_name)

        # Gets the ai type
        ai = data['ai']

        # todo use the inventory type

        # Runs the Entity init method
        super().__init__(floor, x, y, ai=ai, inventory=inventory, obstruct=True)

        # Set the character to not dead
        self.is_dead = False

    def move(self, delta_x, delta_y):
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            if not self.checkEntityObstruct(destination):
                self.x += delta_x
                self.y += delta_y

    def validateMove(self, destination):
        # If destination is out of range
        if destination[0] < 0 or destination[0] >= self.location.width:
            return False
        elif destination[1] < 0 or destination[1] >= self.location.height:
            return False
        # If destination is blocked
        elif not self.location.map.walkable[destination[1]][destination[0]]:
            return False
        else:
            return True

    def checkEntityObstruct(self, destination):
        for entity in self.location.entities:
            if entity is self or not entity.obstruct:
                continue
            elif entity.x == destination[0] and entity.y == destination[1]:
                self.meleeAttack(entity)
                return True
        return False

    def meleeAttack(self, opponent):
        attack = self.getMeleeDamage()
        defense = opponent.getDefense()

        # Determines the damage based on the
        damage = formulas.getDamageDealt(attack, defense)

        # Gets the encumbrance of the two characters
        self_enc = self.getEncumbrance()
        enemy_enc = opponent.getEncumbrance()

        # Determines the hit chance based on the encumbrances
        hit_chance = formulas.getHitChance(self_enc, enemy_enc)

        for attack in range(self.getAttackRate()):
            roll = random.random()
            if roll < hit_chance:
                Log.addMessage(self.name + " hit " + opponent.name + " for " + str(damage) + " damage")
                opponent.takeDamage(damage)
        if opponent.is_dead:
            Log.addMessage(self.name + " killed " + opponent.name)

    def takeDamage(self, damage):
        if not self.energy == 0:

            # If energy exceeds damage, it is completely absorbed by the shields
            if self.energy > damage:
                damage_to_flesh = 0
                self.energy -= damage

            # Otherwise, energy is reduced to zero and difference is dealt to flesh
            else:
                damage_to_flesh = damage - self.energy
                self.energy = 0
                Log.addMessage(self.name + " energy depleted")
        else:
            damage_to_flesh = damage

        # Generator is tagged as being hit this turn
        if self.inventory.equipped['generator']:
            self.inventory.equipped['generator'].hit_this_turn = True

        # Determine if the damage to flesh was lethal
        killed = formulas.determineLethal(damage_to_flesh, self.life)


        if killed:
            self.kill()
        # If self was not killed, determine if injured
        else:
            injured = formulas.determineInjury(damage_to_flesh, self.life)
            if injured:
                Log.addMessage(self.name + " suffered an injury")
                self.life -= 1

    def kill(self):
        """Kills the character. Removes the AI, removes the entity from the map and creates a corpse"""
        self.is_dead = True
        self.ai = None
        self.location.removeEntity(self)
        # Create a corpse
        Corpse(self)
    
    def getDefense(self):
        """Gets the defense based on the base_defense and, if the character has armor, armor defense

        Returns
            defense : int
                An integer representing the defense
        """
        defense = self.base_defense
        if self.inventory and self.inventory.equipped['armor']:
            armor = self.inventory.equipped['armor']
            defense += armor.defense
        return defense
        
    def getMeleeDamage(self):
        damage = self.base_damage
        if self.inventory and self.inventory.equipped['weapon']:
            weapon = self.inventory.equipped['weapon']
            damage += weapon.melee_damage

        return damage

    def getAttackRate(self, ranged=False):
        """Gets the number of attacks that can be performed in a turn

        Parameters:
            ranged : boolean
                represents whether these are ranged attacks or melee attacks

        Returns:
            : int
                Number of attacks that will be performed in a turn
        """
        # Find out if carrying weapon; if not, return base_attack_rate
        if self.inventory and self.inventory.equipped['weapon']:
            weapon = self.inventory.equipped['weapon']
        else:
            return self.base_attack_rate

        # If its a melee attack
        if not ranged:
            return weapon.melee_speed
        else:
            return weapon.fire_rate

    def getEncumbrance(self):
        """Encumbrance determines the penalty to hit chance or dodge chance"""
        encumbrance = 0
        if self.inventory is None:
            pass
        else:
            equipment = self.inventory.equipped
            for item in equipment:
                if equipment[item] is not None and equipment[item].difficulty > self.level:
                    encumbrance += equipment[item].difficulty - self.level

        return encumbrance

    @property
    def energy(self):
        if self.inventory is None or self.inventory.equipped['generator'] is None:
            return 0
        else:
            return self.inventory.equipped['generator'].current_charge
    @energy.setter
    def energy(self, value):
        try:
            self.inventory.equipped['generator'].current_charge = value
        except:
            print("No Generator to hold energy")

    @property
    def max_energy(self):
        if self.inventory.equipped['generator'] is None:
            return 0
        else:
            return self.inventory.equipped['generator'].max_charge


class Player(Character):
    image = pygame.image.load(os.path.join('images','characters','player.png'))
    
    def __init__(self, name, background, floor, x, y):
        """Extends the Character init method

        Parameters:
            name : string
                name of the player
            background : string
                background of the player which determines the starting items
                Valid Attributes are ['officer','marksman','agent','pointman','gladiator']
            floor : Floor
                the starting location of the player
            x : int
                starting x position on the floor
            y : int
                starting y position on the floor
        """

        super().__init__("PLAYER", floor, x, y, inventory=[])

        # Overrides the name set by the Character init method
        self.name = name

        # Stores the background
        assert background in ("Officer","Marksman","Agent","Pointman","Gladiator")
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

    def calculateFOV(self):
        self.location.map.compute_fov(self.x, self.y)

    def getFOV(self):
        return self.location.map.fov

    def discoverTiles(self):
        fov = numpy.where(self.getFOV())
        for i in range(len(fov[0])):
            self.location.tile_map[(fov[1][i])][(fov[0][i])].discovered = True