"""
Contains the classes used to construct actors(player,enemies,items)

Classes:
    Entity
    Target(Entity)
    Portal(Entity)
    Corpse(Entity)
"""

import os, pygame
import random

import numpy

from source.components import AI, Inventory, Camera
from source.constants import CELL_SIZE, BACKGROUNDS
from source.game import Log
from source import formulas
from source.utilities import getItemById, getDistanceBetweenEntities

# Location of the json file which holds the character data
CHARACTER_JSON = os.path.join('data', 'characters.json')
ITEM_JSON = os.path.join('data','items.json')


class Entity:
    """Represents any object that can act and be drawn into the world
    
    Attributes:
        image_path : string
            CLASS; Used to identify relative location of the image file
        CELL_SIZE : int
            CLASS; The number of pixels in the width and height of each image
        x : int or None
            X location on the tile map. Should be None if not on a tile map
        y : int or None
            Y location on the tile map. Should be None if not on a tile map
        location : Floor or Inventory
            where the entity is found in the game
        obstruct : bool
            Whether the entity stops another entity from moving through it.
            Typically, Characters should have this set to true and everything else should be false
        image : pygame.Surface
            the entity's image as a Surface object
        ai : AI or None
            the entity's AI component if it has one
        inventory : Inventory or None
            the entity's Inventory component if it has one
    
    Methods:
        loadImage(self) : Loads the image stored at the image_path attribute
        draw(self) : Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates
    
    Children:
        Corpse(Entity)
        Item(Entity)
            Armor(Item)
            Weapon(Item)
            Armor(Item)
            Battery(Item)
        Character(Entity)
            Player(Character)
    """
    
    # Default image_path value for all entities
    image_path = os.path.join('images', 'unknown.png')
    CELL_SIZE = CELL_SIZE

    def __init__(self, location, x=None, y=None, ai=None, inventory=None, obstruct=False, is_player=False):
        """Init method for Entity
        
        Parameters: 
            location : Floor or Inventory
                where the entity is found in the game
            x : int
                X location on the tile map. Should be None if not on a tile map
            y : int
                Y location on the tile map. Should be None if not on a tile map
            ai : None or True
            inventory : None or List
            obstruct : bool
                Whether the entity obtructs movement or not
        """
        self.x = x
        self.y = y
        self.location = location
        self.location.addEntity(self)
        self.obstruct = obstruct
        self.image = None
        self.discovered = False
        self.last_known_x = None
        self.last_known_y = None
        if is_player:
            self.is_player = True
        else:
            self.is_player = False

        if ai:
            self.ai = AI(self, ai)
        else:
            self.ai = None
        
        if inventory is not None:
            self.inventory = Inventory(self, inventory)
        else:
            self.inventory = None

    def loadImage(self):
        """Loads the image stored at the image_path attribute

        Requires pygame to be initialized"""
        self.image = pygame.image.load(self.image_path).convert_alpha()

    def draw(self, surface):
        """Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates

        Requires pygame to be initialized

        Paramaters:
            surface : pygame.Surface
                The surface that the image will get written to
        """
        # First load the image if it hasn't been loaded
        if self.image is None:
                self.loadImage()
        surface.blit(self.image, (self.x*self.CELL_SIZE, self.y*self.CELL_SIZE))

    def drawAtLastKnown(self, surface):
        """Draws the entity at the last known location rather than necessarily the actual location"""
        surface.blit(self.image, (self.last_known_x*self.CELL_SIZE, self.last_known_y*self.CELL_SIZE))


class Target(Entity):
    """Represents the player's target when aiming or exploring"""
    image_path = os.path.join('images','other','target.png')
    def move(self, delta_x, delta_y):
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            self.x += delta_x
            self.y += delta_y

    def remove(self):
        self.location.removeEntity(self)

    def validateMove(self, destination):
        """Validates the move for the target entity to ensure it does not move out of bounds"""
        floor_width = self.location.width
        floor_height = self.location.height

        if destination[0] in range(0, floor_width) and destination[1] in range(0, floor_height):
            return True
        else:
            return False

    @property
    def on_top_of(self):
        floor = self.location
        for entity in floor.entities:
            if not entity.obstruct:
                continue
            elif self.x == entity.x and self.y == entity.y:
                return entity

        # If for loop finds no match
        return None

    @on_top_of.setter
    def on_top_of(self, entity):
        self.x = entity.x
        self.y = entity.y


class Portal(Entity):
    """Entity used to move player between floors"""

    def __init__(self, location, x, y, direction):
        super().__init__(location, x, y)
        assert direction in ("up", "down")
        if direction == "down":
            self.image_path = os.path.join('images', 'other', 'down_portal.png')
        else:
            self.image_path = os.path.join('images', 'other', 'up_portal.png')
        self.direction = direction


class Corpse(Entity):
    """This is created when a character object has been killed
    
    Child of Entity
    
    Attributes:
        image_path : string
            INHERITED, CLASS; Used to identify relative location of the image file
        CELL_SIZE : int
            INHERITED, CLASS; The number of pixels in the width and height of each image
        x : int or None
            INHERITED; X location on the tile map. Should be None if not on a tile map
        y : int or None
            INHERITED; Y location on the tile map. Should be None if not on a tile map
        location : Floor
            INHERITED; what floor the corpse is found in the game
        obstruct : bool
            INHERITED; Whether the entity stops another entity from moving through it. 
            Should be False for Corpses
        image : pygame.Surface
            INHERITED; the corpse's image as a Surface object
        ai : None
            INHERITED; Specifies that corpse does not have ai
        inventory : Inventory
            INHERITED; the corpse's Inventory component
    """

    image_path = os.path.join('images', 'other', 'headstone.png')
    def __init__(self, character):
        """Init method for Corpse. Extends the init method of Entity
        
        
        Parameters:
            character : Character
                The character that died this is make this corpse
        """
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.location, character.x, character.y, inventory=inventory_contents)


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
        is_dead : bool

    Methods:
        loadImage(self) : INHERITED
        draw(self) : INHERITED

    Properties:
        energy : int : RW; Amount of energy in the Character's Generator
        max_energy : int : RO; Amount of energy that a Character's Generator could hold

    Children:
        Player(Character)"""
    def __init__(self, char_id, floor, x, y, inventory=[], is_player=False):
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
        super().__init__(floor, x, y, ai=ai, inventory=inventory, obstruct=True, is_player=is_player)

        # Set the character to not dead
        self.is_dead = False

    def move(self, delta_x, delta_y, peacefully=False):
        """Moves the character by specified x and y values"""
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            entity_at_dest = self.checkEntityObstruct(destination)
            if entity_at_dest is None:
                self.x += delta_x
                self.y += delta_y
            elif not peacefully:
                self.meleeAttack(entity_at_dest)

    def validateMove(self, destination):
        """Returns True if the destination is walkable and False if it isn't"""
        # Reminder: Floor.map.walkable uses row major order
        if self.location.map.walkable[destination[1]][destination[0]]:
            return True
        else:
            return False

    def checkEntityObstruct(self, destination):
        """Checks if an obstructing entity is in the destination. If it is, return it

        Parameters:
            destination : 2-tuple of ints : (x,y) format
            peacefully : boolean : If true, does not attack

        Returns:
            None or Entity : Entity that is obstructing the move

         """
        for entity in self.location.entities:
            if entity is self or not entity.obstruct:
                continue
            elif entity.x == destination[0] and entity.y == destination[1]:
                return entity

    def meleeAttack(self, opponent):
        """Attacks a specified opponent with a melee attack

        Parameters:
            opponent : Character
        """
        attack = self.getMeleeDamage()
        defense = opponent.getDefense()

        # Determines the damage based on the attack and defense
        damage = formulas.getDamageDealt(attack, defense)

        # Gets the encumbrance of the two characters
        self_enc = self.getEncumbrance()
        enemy_enc = opponent.getEncumbrance()

        # Determines the hit chance based on the encumbrances
        hit_chance = formulas.getMeleeHitChance(self_enc, enemy_enc)

        # For every attack in the quantity of attack rate...
        for attack in range(self.getAttackRate()):
            # Roll to determine if attack landed
            roll = random.random()
            if roll < hit_chance:
                Log.addToBuffer(self.name + " hit " + opponent.name + " for " + str(damage) + " damage")
                opponent.takeDamage(damage)
        # Send a message if the opponent was killed
            if opponent.is_dead:
                Log.addToBuffer(self.name + " killed " + opponent.name)
                break

    def rangedAttack(self, opponent):
        """Attacks a specified opponent with a ranged attack"""
        attack = self.getRangedDamage()
        defense = opponent.getDefense()

        # Determines the damage based on the attack and defense
        damage = formulas.getDamageDealt(attack, defense)

        # Gets the encumbrance of the two characters
        self_enc = self.getEncumbrance()
        enemy_enc = opponent.getEncumbrance()
        
        # Find the range exceeded by getting the distance between then subtracting the range
        range_exceeded = getDistanceBetweenEntities((self.x,self.y),(opponent.x,opponent.y)) - self.getWeaponRange()
        if range_exceeded < 0:
            range_exceeded = 0
        
        # Determines the hit chance based on the encumbrances
        hit_chance = formulas.getRangedHitChance(self_enc, enemy_enc, range_exceeded)

        # For every attack in the quantity of attack rate...
        for attack in range(self.getAttackRate(ranged=True)):
            if self.energy > self.getEnergyPerShot():
                # Reduce current energy
                self.energy -= self.getEnergyPerShot() - self.getRecoilCharge()

                # Roll to determine if attack landed
                roll = random.random()
                if roll < hit_chance:
                    Log.addToBuffer(self.name + " hit " + opponent.name + " for " + str(damage) + " damage")
                    opponent.takeDamage(damage)

                # Send a message if the opponent was killed
                if opponent.is_dead:
                    Log.addToBuffer(self.name + " killed " + opponent.name)
                    break

    def takeDamage(self, damage):
        """Reduces the amount of energy in the character's generator and deals any remaining to flesh

        Attacks to flesh do not nessearilly reduce life points but rather affect the chance to kill or chance to injure

        Paramaters:
            damage : int
        """
        # If the character has some energy, damage is dealt to it first
        if not self.energy == 0:

            # If energy exceeds damage, it is completely absorbed by the shields
            if self.energy > damage:
                damage_to_flesh = 0
                self.energy -= damage

            # Otherwise, energy is reduced to zero and difference is dealt to flesh
            else:
                damage_to_flesh = damage - self.energy
                self.energy = 0
                Log.addToBuffer(self.name + " energy depleted")
        else:
            damage_to_flesh = damage

        # Generator is tagged as being hit this turn
        if self.inventory.equipped['generator']:
            self.inventory.equipped['generator'].hit_this_turn = True

        # Determine if the damage to flesh was lethal
        killed = formulas.determineLethal(damage_to_flesh, self.life)

        # If killed, run kill method on self
        if killed:
            self.kill()

        # If self was not killed, determine if injured
        else:
            injured = formulas.determineInjury(damage_to_flesh, self.life)

            # If injured, log message and reduce life by 1
            if injured:
                Log.addToBuffer(self.name + " suffered an injury")
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
        """Gets the amount of melee damage that a character can deal per attack including weapon damage"""
        damage = self.base_damage
        if self.inventory and self.inventory.equipped['weapon']:
            weapon = self.inventory.equipped['weapon']
            damage += weapon.melee_damage

        return damage

    def getRangedDamage(self):
        if self.inventory.equipped['weapon'] and self.inventory.equipped['weapon'].is_ranged:
            return self.inventory.equipped['weapon'].ranged_damage

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

    def getEnergyPerShot(self):
        """The energy that every shot uses"""
        return self.inventory.equipped['weapon'].energy_per_shot

    def getRecoilCharge(self):
        """The amount of energy that is recycled back into the generator after every shot"""
        if self.getEnergyPerShot() < self.inventory.equipped['generator'].recoil_charge:
            return self.getEnergyPerShot()
        else:
            return self.inventory.equipped['generator'].recoil_charge

    def getWeaponRange(self):
        """The range of the currently equipped ranged weapon"""
        return self.inventory.equipped['weapon'].range

    @property
    def energy(self):
        """Amount of energy currently in the character's generator

        Returns: int
        """
        if self.inventory is None or self.inventory.equipped['generator'] is None:
            return 0
        else:
            return self.inventory.equipped['generator'].current_charge

    @energy.setter
    def energy(self, value):
        """Setter method for energy"""
        try:
            self.inventory.equipped['generator'].current_charge = value
        except:
            print("No Generator to hold energy")

    @property
    def max_energy(self):
        """Amount of energy the character's generator could hold

        Returns:: int"""
        if self.inventory.equipped['generator'] is None:
            return 0
        else:
            return self.inventory.equipped['generator'].max_charge




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
        assert background in BACKGROUNDS
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


class Item(Entity):
    """Represents entities which can be inside of an Inventory

    Child of Entity

    Attributes:


    Methods:
        drop(self) : Item is moved from inventory to floor
        pickUp(self) : Item is moved from floor to specified Inventory
    """

    def drop(self):
        """Item is moved from inventory to floor"""
        self.location.removeEntity(self)
        self.x = self.location.owner.x
        self.y = self.location.owner.y

        # The destination floor is the inventory's owner's location
        floor = self.location.owner.location

        # Add entity to floor
        floor.addEntity(self)
        self.location = floor

    def pickUp(self, inventory):
        """Item is moved from floor to specified Inventory"""
        self.location.removeEntity(self)
        self.x = None
        self.y = None
        self.location = inventory
        inventory.addEntity(self)


class Weapon(Item):
    """Damage dealing item which can be equipped

    Child of Item, Entity

    """
    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)

        data = getItemById(ITEM_JSON, item_id, "WEAPONS")

        self.name = data['name']
        self.melee_damage = data['melee_damage']
        self.melee_speed = data['melee_speed']
        self.is_quick_draw = data['quick_draw']
        self.difficulty = data['difficulty']
        self.is_ranged = bool(data['ranged'])
        if self.is_ranged:
            self.ranged_damage = data['ranged']['damage']
            self.energy_per_shot = data['ranged']['energy']
            self.fire_rate = data['ranged']['fire_rate']
            self.range = data['ranged']['range']

    def equip(self):
        self.location.equipped['weapon'] = self


class Armor(Item):
    """Item which provides defense when equipped

    Child of Item, Entity


    """
    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)

        data = getItemById(ITEM_JSON, item_id, "ARMOR")

        self.name = data['name']
        self.defense = data['defense']
        self.difficulty = data['difficulty']

    def equip(self):
        self.location.equipped['armor'] = self


class Generator(Item):
    """"Item which provides energy when equipped

    Child of Item, Entity

    """

    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)

        data = getItemById(ITEM_JSON, item_id, "GENERATORS")

        self.name = data['name']
        self.max_charge = data['max_charge']
        self.recharge_rate = data['recharge_rate']
        self.recoil_charge = data['recoil_charge']
        self.difficulty = data['difficulty']


        self.hit_this_turn = False

        # Current Charge Starts at 0
        self.current_charge = 0.0

    def equip(self):
        self.location.equipped['generator'] = self
        self.current_charge = 0.0

    def recharge(self):
        # Happens once per turn while equipped if not hit this turn
        if not self.hit_this_turn:
            new_charge_level = self.current_charge + self.recharge_rate
            if new_charge_level > self.max_charge:
                self.current_charge = self.max_charge
            else:
                self.current_charge = new_charge_level

    def rechargeToFull(self):
        self.current_charge = self.max_charge


class Battery(Item):
    """Item which can be used to charge energy

    Child of Item, Entity


    """

    def __init__(self, item_id, location, x=None, y=None):
        """Extends the Entity init method"""
        super().__init__(location, x, y)

        data = getItemById(ITEM_JSON, item_id, "BATTERIES")

        self.name = data['name']
        self.power = data['power']


    def use(self):
        target = self.location.equipped['generator']
        target.current_charge += self.power


