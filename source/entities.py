"""
Contains the classes used to construct entities (player,enemies,items, etc.)

Classes:
    Entity
    Target(Entity)
    Portal(Entity)
    Corpse(Entity)
    Character(Entity)
    Player(Character)
    Item(Entity)
    Weapon(Item)
    Armor(Item)
    Reactor(Item)
    Battery(Item)
    
"""
# Standard Library
import random
# Third Party
import numpy
import pygame
# My Modules
from source import formulas
from source.components import AI, Inventory, Camera
from source.constants import CELL_SIZE, BACKGROUNDS, COLORS, DRAW_ORDER
from source.game import Log
from source.utilities import getDistanceBetweenEntities, getLineBetweenEntities
from source.assets import Images, Data
from source.projectile import Projectile


class Entity:
    """Represents any object that can act and be drawn into the world
    
    Attributes:
        image_dir : string : CLASS; Used to identify relative location of the image file
        image_name : string : CLASS; identifier of the image file
        x : int or None : X location on the tile map. Should be None if not on a tile map
        y : int or None : Y location on the tile map. Should be None if not on a tile map
        location : Floor or Inventory
        obstruct : bool : Whether the entity stops another entity from moving through it.
            Typically, Characters should have this set to true and everything else should be false
        image : pygame.Surface
        discovered : bool : Whether the player has seen the entity before or not
        last_known_x : int : Last known x location on the tile map
        last_known_y : int : Last known y location on the tile map
        is_player : bool
        ai : AI or None
        inventory : Inventory or None
    
    Methods:
        draw(self) : Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates
        drawAtLastKnown(self) : Similar to draw but at the lastKnown x and y
    
    Children:
        Corpse(Entity)
        Target(Entity)
        Portal(Entity)
        Item(Entity)
            Armor(Item)
            Weapon(Item)
            Armor(Item)
            Battery(Item)
        Character(Entity)
            Player(Character)
    """

    # Default image_path value for all entities
    image_dir = None
    image_name = None

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
        self.image = Images.getImage(self.image_dir, self.image_name)
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

    def draw(self, surface):
        """Takes a pygame surface object and blits the object's 'image' to it at the determined x and y coordinates

        Requires pygame to be initialized

        Paramaters:
            surface : pygame.Surface
                The surface that the image will get written to
        """
        surface.blit(self.image, (self.x*CELL_SIZE, self.y*CELL_SIZE))

    def drawAtLastKnown(self, surface):
        """Draws the entity at the last known location rather than necessarily the actual location"""
        surface.blit(self.image, (self.last_known_x*CELL_SIZE, self.last_known_y*CELL_SIZE))


class Target(Entity):
    """Represents the player's target when aiming or exploring"""
    image_dir = 'Other'
    image_name = 'target'
    draw_order = DRAW_ORDER['TARGET']
    
    def __init__(self, floor, x, y, origin):
        self.origin = origin
        super().__init__(floor, x, y)

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

    def drawPath(self, surface):
        path = self.getPath()
        for tile in path:
            # Stop drawing if path blocked or not in FOV
            if not self.location.map.walkable[tile[1]][tile[0]] or not self.location.map.fov[tile[1]][tile[0]]:
                break
            surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
            surf.set_alpha(64)
            surf.fill(COLORS['RED'])
            surface.blit(surf, (tile[0]*CELL_SIZE, tile[1]*CELL_SIZE))
    
    def getPath(self):
        if self.location.map.fov[self.y][self.x] and self.location.map.walkable[self.y][self.x]:
            return self.location.path_finder.get_path(self.origin.x, self.origin.y, self.x, self.y)
        else:
            return getLineBetweenEntities((self.origin.x, self.origin.y,), (self.x, self.y))

    def getFirstInPath(self):
        """Returns the first entity in the path or none if there are no entities in the path"""
        path = self.getPath()
        for tile in path:
            for entity in self.location.entities:
                if not entity.obstruct:
                    continue
                elif tile[0] == entity.x and tile[1] == entity.y:
                    return entity

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
    image_dir = 'Other'
    draw_order = DRAW_ORDER['PORTAL']

    def __init__(self, location, x, y, direction):
        assert direction in ("up", "down")
        if direction == "down":
            self.image_name = 'down_portal'
        else:
            self.image_name = 'up_portal'
        self.direction = direction
        super().__init__(location, x, y)


class Corpse(Entity):
    """This is created when a character object has been killed
    
    Child of Entity
    
    Attributes:
        image_dir : string : CLASS; Used to identify relative location of the image file
        image_name : string : CLASS; 
        x : int : INHERITED; X location on the tile map.
        y : int : INHERITED; Y location on the tile map. Should be None if not on a tile map
        location : Floor : INHERITED; what floor the corpse is found in the game
        obstruct : bool : INHERITED; Whether the entity stops another entity from moving through it. 
            Should be False for Corpses
        image : pygame.Surface : INHERITED; the corpse's image as a Surface object
        ai : None : INHERITED; Specifies that corpse does not have ai
        inventory : Inventory : INHERITED; the corpse's Inventory component
    """

    image_dir = 'Other'
    image_name = 'headstone'
    draw_order = DRAW_ORDER['CORPSE']
    
    def __init__(self, character):
        """Init method for Corpse. Extends the init method of Entity
        
        
        Parameters:
            character : Character
                The character that died this is make this corpse
        """
        self.name = character.name
        super().__init__(character.location, character.x, character.y)


class Character(Entity):
    """Used for entities which act on the world (ie Enemies and the Player)

    Child of Entity

    Attributes:
        image_dir : string : CLASS; 
        image_name : string 
        x : int : INHERITED
        y : int : INHERITED
        location : Floor : INHERITED
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
        draw(self) : INHERITED
        move(self, delta_x, delta_y, peacefully=False) : Moves the characer by the specified x and y values
        validateMove(self, destination) : Returns True if the destination is walkable and False if it isn'tagged
        checkEntityObstruct(self, destination) : Checks if an obstructing entity is in the destination.
        attack(self, opponent, is_ranged=False) : Attacks a specified opponent
        takeDamage(self, damage) : Reduces the amount of energy in the characters reactor and deals any remaining to flesh
        kill(self) : Kill the character
        getDefense(self) : Gets the total defense of the character
        getMeleeDamage(self) : Gets the total melee damage per strike
        getRangedDamage(self) : Gets the ranged damage per shot
        getAttackRate(self, is_ranged=False) : Gets the number of attacks that can be performed in a turn
        getEncumbrance(self) : The amount that equipment outlevels character
        getEnergyPerShot(self) : The energy that every shot uses
        getRecoilCharge(self) : The amount of energy that is recycled back into the reactor after every shot
        getWeaponRange(self) 
        getMeleeVerb(self) : Gets the verb to describe a melee attack
        getRangedVerb(self) : Gets the verb to describe a ranged attack
        
    Properties:
        energy : int : RW; Amount of energy in the Character's Reactor
        max_energy : int : RO; Amount of energy that a Character's Reactor could hold

    Children:
        Player(Character)"""
        
    image_dir = 'Characters'
    draw_order = DRAW_ORDER['ENEMY']

    def __init__(self, char_id, floor, x, y, is_player=False):
        """Extends the entity init function
        
        Uses the char_id to pull data, represented as a dict, from the Data class"""

        # Gets the data from the JSON File
        data = Data.getCharacter(char_id)

        # Copies the info from the data
        self.name = data['name']
        self.level = data['level']
        self.melee_verb = data['verb']
        self.xp = data['xp']
        self.life = data['life']
        self.base_damage = data['damage']
        self.base_defense = data['defense']
        self.base_attack_rate = data['attack_rate']
        self.innate_ranged = bool(data['innate_ranged'])
        if self.innate_ranged:
            self.ranged_verb = data['innate_ranged']['verb']
            self.ranged_damage = data['innate_ranged']['damage']
            self.range = data['innate_ranged']['range']
            self.ranged_attack_rate = data['innate_ranged']['rate']
            self.projectile = data['innate_ranged']['projectile']
        
        # Gets the image
        self.image_name = data['image']

        # Gets the ai type
        ai = data['ai']

        # Gets the inventory type
        inventory = data['inventory']

        # Ensure that every character gets an empty inventory instead of no inventory
        if inventory is None:
            inventory = "empty"

        # Runs the Entity init method
        super().__init__(floor, x, y, ai=ai, inventory=inventory, obstruct=True, is_player=is_player)

        # Set the character to not dead
        self.is_dead = False

    def move(self, delta_x, delta_y, peacefully=False):
        """Moves the character by specified x and y values

        Returns: bool : Indicates whether a movement or other action was taken"""
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            entity_at_dest = self.checkEntityObstruct(destination)
            if entity_at_dest is None:
                self.x += delta_x
                self.y += delta_y
                return True
            elif not peacefully:
                self.attack(entity_at_dest)
                return True
            else:
                return False
        else:
            return False

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

        Returns:
            None or Entity : Entity that is obstructing the move

         """
        for entity in self.location.entities:
            if entity is self or not entity.obstruct:
                continue
            elif entity.x == destination[0] and entity.y == destination[1]:
                return entity
    
    def attack(self, opponent, is_ranged=False):
        """Attack a specified opponent
        
        Paramaters:
            opponent: Character
            is_ranged : bool
        
        Calls:
            Character.getDefense()
            Character.getEncumbrance()
            Character.getRangedDamage()
            Character.getWeaponRange()
            Character.getRangedVerb()
            Character.getMeleeDamage()
            Character.getMeleeVerb()
            Character.getAttackRate(is_ranged)
            Character.getEnergyPerShot()
            Character.getRecoilCharge()
            Character.takeDamage(damage)
            formulas.getDamageDealt(attack, defense)
            formulas.getMeleeHitChance(attacker_enc, defender_enc)
            formualas.getRangedHitChance(attacker_enc, defender_enc, range_exceeded)
            utilities.getDistanceBetweenEntities(coordsA, coordsB)
            game.Log.addToBuffer(message)
            random.random()
        
        Returns: None
        """
        # Get defense of opponent character
        defense = opponent.getDefense()
        
        # Get the encumbrance of both characters
        self_enc = self.getEncumbrance()
        oppo_enc = opponent.getEncumbrance()

        # Get attack, hit_chance, and verb depending if ranged to melee attack
        if is_ranged:
            attack = self.getRangedDamage()
            
            # Gets the difference between the distance and the maximum range and sets it to at least 0
            range_exceeded = getDistanceBetweenEntities((self.x, self.y), (opponent.x, opponent.y)) - self.getRange()
            if range_exceeded < 0: 
                range_exceeded = 0
            
            hit_chance = formulas.getRangedHitChance(self_enc, oppo_enc, range_exceeded)
            verb = self.getRangedVerb()
           
        else:
            attack = self.getMeleeDamage()
            hit_chance = formulas.getMeleeHitChance(self_enc, oppo_enc)
            verb = self.getMeleeVerb()

        # Calculate the damage
        damage = formulas.getDamageDealt(attack, defense)
        
        # Boolean that determines if energy is being used on the attack
        using_energy = bool(is_ranged and self.inventory.equipped['weapon'])
        
        # For every strike in the number of attacks...
        for strike in range(self.getAttackRate(is_ranged)):
            if using_energy and self.energy >= self.getEnergyPerShot():
                # Reduce current energy
                self.energy -= self.getEnergyPerShot() - self.getRecoilCharge()
            elif using_energy:
                # using_energy but doesn't have enough energy
                Log.addToBuffer("Not enough Energy")
                break
            
            # rolls random float 0-1 to determine if attack landed
            roll = random.random()
            
            # If attack landed deal damage to opponent and add message to Buffer
            if roll < hit_chance:
                Log.addToBuffer("%s %s %s (%.1f dmg)" % (self.name, verb, opponent.name, damage))
                opponent.takeDamage(damage)
            else:
                Log.addToBuffer(self.name + " missed")
            
            if is_ranged:
                # Create Projectile
                projectile_id = self.getProjectile()
                Projectile(projectile_id, self.location, (self.x, self.y), (opponent.x, opponent.y), delay=strike*5)

            # Send a message if the opponent was killed
            if opponent.is_dead:
                try:
                    self.collectXP(opponent)
                except AttributeError:
                    pass
                Log.addToBuffer("%s killed %s" % (self.name, opponent.name))
                break

        # END FOR STRIKE LOOP
         
    def takeDamage(self, damage):
        """Reduces the amount of energy in the character's reactor and deals any remaining to flesh

        Attacks to flesh do not nessearilly reduce life points but rather affect the chance to kill or chance to injure

        Paramaters:
            damage : int
        """
        # If the character has some energy, damage is dealt to it first
        if not self.energy == 0:

            # If energy exceeds damage, it is completely absorbed by the shields
            if self.energy > damage:
                self.energy -= damage
                return

            # Otherwise, energy is reduced to zero and difference is dealt to flesh
            else:
                self.energy = 0
                Log.addToBuffer(self.name + "'s shield shattered!")
                return
        else:
            damage_to_flesh = damage

        # Reactor is tagged as being hit this turn
        if self.inventory.equipped['reactor']:
            self.inventory.equipped['reactor'].hit_this_turn = True

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
                self.location.tile_map[self.x][self.y].addSplatter()
                Log.addToBuffer(self.name + " was weakened")
                self.life -= 1

    def kill(self):
        """Kills the character. Removes the AI, removes the entity from the map and creates a corpse"""
        self.is_dead = True
        self.ai = None
        self.location.removeEntity(self)
        self.inventory.dropAll()
        # Create a corpse
        Corpse(self)

    def getDefense(self):
        """Gets the defense based on the base_defense and, if the character has armor, armor defense

        Returns: int
        """
        defense = self.base_defense
        if self.inventory.equipped['armor']:
            defense += self.inventory.equipped['armor'].defense
            
        return defense

    def getMeleeDamage(self):
        """Gets the amount of melee damage that a character can deal per attack including weapon damage
        
        Melee damage is the character's base damage plus melee damage on the weapon if it is equipped
        
        Returns: int or float"""
        damage = self.base_damage
        if self.inventory.equipped['weapon']:
            damage += self.inventory.equipped['weapon'].melee_damage

        return damage

    def getRangedDamage(self):
        """Gets the damage of a ranged attack
        
        Ranged attack is the ranged_damage on the weapon if it is equipped
        
        Returns: int or float
        """
        if self.inventory.equipped['weapon'] and self.inventory.equipped['weapon'].is_ranged:
            return self.inventory.equipped['weapon'].ranged_damage
        else:
            return self.ranged_damage

    def getAttackRate(self, is_ranged=False):
        """Gets the number of attacks that can be performed in a turn

        Parameters:
            is_ranged : boolean
                represents whether these are ranged attacks or melee attacks

        Returns: int
        """

        # Get Weapon
        weapon = self.inventory.equipped['weapon']

        # If its a ranged attack
        if is_ranged:
            if weapon is not None and weapon.is_ranged:
                return weapon.fire_rate
            else:
                return self.ranged_attack_rate

        # If is a melee attack
        else:
            if weapon:
                return weapon.melee_speed
            else:
                return self.base_attack_rate

    def getEncumbrance(self):
        """Encumbrance determines the penalty to hit chance or dodge chance
        
        It is calculated by determining the amount that the difficulty of  equipment item exceeds the level of the
        character
        
        Returns : int"""
        encumbrance = 0
        equipment = self.inventory.equipped
        for item in equipment:
            if equipment[item] is not None and equipment[item].difficulty > self.level:
                encumbrance += equipment[item].difficulty - self.level

        return encumbrance

    def getEnergyPerShot(self):
        """The energy that every shot uses
        
        If a the character does not have a ranged weapoon equipped, then return 0"""
        try:
            return self.inventory.equipped['weapon'].energy_per_shot
        except AttributeError:
            return 0

    def getRecoilCharge(self):
        """The amount of energy that is recycled back into the reactor after every shot.
        
        This is either the amount of energy per shot on the equipped weapon or the recoil charge on the reactor,
        whichever is lower
        
        Returns: float
        """
        try:
            if self.getEnergyPerShot() < self.inventory.equipped['reactor'].recoil_charge:
                return self.getEnergyPerShot()
            else:
                return self.inventory.equipped['reactor'].recoil_charge
        except AttributeError:
            return 0

    def getRange(self):
        """The range of the currently equipped ranged weapon or if no ranged weapon equipped, the innate range"""
        if self.inventory.equipped['weapon'] is not None and self.inventory.equipped['weapon'].is_ranged:
            return self.inventory.equipped['weapon'].range
        else:
            return self.range
    
    def getMeleeVerb(self):
        """Get the verb used to describe the melee attack (e.g. 'hit')
        
        Gets the verb on the weapon if one is equipped, otherwise gets the verb from the character
        
        Returns: string
        """
        if self.inventory.equipped['weapon'] is not None:
            return self.inventory.equipped['weapon'].melee_verb
        else:
            return self.melee_verb

    def getRangedVerb(self):
        """Get the verb used to describe the ranged attack (e.g.'shoot')
        
        Returns: string
        """
        if self.inventory.equipped['weapon'] is not None and self.inventory.equipped['weapon'].is_ranged:
            return self.inventory.equipped['weapon'].ranged_verb
        else:
            return self.ranged_verb

    def getProjectile(self):
        """Returns a string representing the projectile id"""
        try:
            return self.inventory.equipped['weapon'].projectile
        except AttributeError:
            return self.projectile

    def draw(self, surface):
        """Extends the entity draw function to draw a forcefield if the character has energy"""
        super().draw(surface)

        if self.energy > 0:
            force_field = Images.getImage('Other', 'force_field')
            surface.blit(force_field, (self.x*CELL_SIZE, self.y*CELL_SIZE))

    @property
    def energy(self):
        """Amount of energy currently in the character's reactor

        Returns: int
        """
        if self.inventory.equipped['reactor'] is None:
            return 0
        else:
            return self.inventory.equipped['reactor'].current_charge

    @energy.setter
    def energy(self, value):
        """Setter method for energy"""
        self.inventory.equipped['reactor'].current_charge = value

    @property
    def max_energy(self):
        """Amount of energy the character's reactor could hold

        Returns:: int"""
        if self.inventory.equipped['reactor'] is None:
            return 0
        else:
            return self.inventory.equipped['reactor'].max_charge


class Player(Character):
    """Class which defines the Player Character
    
    Child of Character
    """
    draw_order = DRAW_ORDER['PLAYER']
    base_image = None

    xp_ceiling = [0, 1, 5, 10, 15, 25]

    max_level = len(xp_ceiling)

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

        super().__init__("PLAYER", floor, x, y, is_player=True)

        # Overrides the name set by the Character init method
        self.name = name

        # Stores the background
        assert background in BACKGROUNDS
        self.background = background

        # Player-Specific Component
        self.camera = Camera(self)

        # Overrides what is defined in parent init functions
        self.inventory = Inventory(self, self.background)

        # Start with a calculated FOV
        self.calculateFOV()
        self.discoverTiles()

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
    
    def lookAround(self):
        """Returns a string indicating observations about the entities around the player
        
        Utilizes the draw order of the items to look through them in reverse order
        
        Message Priority
            Enemy(s) in FOV
            Item(s) at Feet
            Portal at Feet
            Corpse(s) at Feet
            Item(s) in FOV
            Down Portal in FOV
            Up Portal in FOV
        
        Returns : string
        """
    
        # Number of enemies seen in the player's fov
        enemy_count = 0
        enemy = None
        
        items_in_view = 0
        items_at_feet = 0
        item_at_feet = None
        item_in_view = None
        
        on_down_portal = False
        on_up_portal = False
        
        see_down_portal = False
        see_up_portal = False
        
        corpses_at_feet = 0
        corpse = None
            
        fov_map = self.getFOV()
        
        # Reversed because characters have higher draw order
        for entity in reversed(self.location.entities):
            if entity is self:
                continue
             
            if fov_map[entity.y][entity.x]:
                if isinstance(entity, Character):
                    enemy_count += 1
                    enemy = entity
                
                # After characters are counted, break if there was at least one
                elif enemy_count > 0:
                    break
                
                elif isinstance(entity, Item):
                    if entity.x == self.x and entity.y == self.y:
                        items_at_feet += 1
                        item_at_feet = entity
                    
                    else:
                        items_in_view += 1
                        item_in_view = entity
                
                # Break if items at feet since it takes priority over Portals
                elif items_at_feet:
                    break
                
                # Is only broken if directly on Portal, otherwise tracks and keep going to corpses
                elif isinstance(entity, Portal):
                    if entity.x == self.x and entity.y == self.y:
                        if entity.direction == "down":
                            on_down_portal = True
                            break
                        else:
                            on_up_portal = True
                            break
                    else:
                        if entity.direction == "down":
                            see_down_portal = True
                        else:
                            see_up_portal = True

                elif isinstance(entity, Corpse):
                    if entity.x == self.x and entity.y == self.y:
                        corpses_at_feet += 1
                        corpse = entity
                        
        # After searching, return proper string
        if enemy_count > 1:
            return "I better be careful. There are %d enemies around" % enemy_count
        if enemy_count == 1:
            return "I see an enemy %s here" % enemy.name
        
        if items_at_feet > 1:
            return "There's a bunch of stuff right here"
        
        if items_at_feet == 1:
            return "There's a %s right here. It could be useful" % item_at_feet.name
            
        if on_down_portal:
            return "Here's the portal to the next floor. I wonder what dangers await me"
        
        if on_up_portal:
            if self.location.number == 1:
                return "Here's the entrance. I don't want to chicken out now"
            else:
                return "Here's the way back to the last floor. Did I forget anything back there?"
        
        if corpses_at_feet > 2:
            return "There's a pile of bodies here. I'm glad that I'm not one of them"
            
        if corpses_at_feet == 2:
            return "There's a couple of bodies here. Better them than me"
        
        if corpses_at_feet == 1:
            return "'Here lies %s' One less obstacle on the path to victory" % corpse.name
        
        if items_in_view > 1:
            return "I see some items over there. Surely one of them will be useful"
        
        if items_in_view == 1:
            return "I see a  %s over there. I wonder if I could put that to use" % item_in_view.name

        if see_down_portal:
            return "Coast looks clear to move to the next floor. Just got to make sure I am ready"
        
        if see_up_portal:
            if self.location.number == 1:
                return "There's the entrance to the trial. No looking back now"
            else:
                return "I should run back to that portal if I think I'm in danger"
        
        # If nothing else was returned
        return "I don't see anything interesting around here. Better keep exploring"

    def getItemsAtFeet(self):
        """Returns a list of items which match the player's x and y coordinates"""
        items = list()
        for entity in self.location.entities:
            if not entity.draw_order == DRAW_ORDER['ITEM']:
                continue
            if entity.x == self.x and entity.y == self.y:
                items.append(entity)

        return items

    def collectXP(self, enemy):
        """Collects the XP that the enemy has

        Parameters:
            enemy: Character"""
        self.xp += enemy.xp

        while not self.level == self.max_level and self.xp >= self.xp_ceiling[self.level]:
            self.levelUp()

    def levelUp(self):
        """Levels up the player

        Every three levels, grants 1 life point

        Every 5 levels grants 1 point base_damage and 1 point base_defense
        """

        Log.addToBuffer("%s leveled up!" % self.name)
        self.level += 1
        if self.level % 3 == 0:
            Log.addToBuffer("%s has become more resilient" % self.name)
            self.life += 1
        if self.level % 5 == 0:
            Log.addToBuffer("%s has become stronger" % self.name)
            self.base_damage += 1
            self.base_defense += 1
        if self.level == self.max_level:
            Log.addToBuffer("%s has reached max level" % self.name)

    def getPercentToNextLevel(self):
        """Returns a floating point number between 0 and 1 that indicates how close the player is to the next level"""
        if self.level == self.max_level:
            return 1.0
        else:
            ceiling_last_lvl = self.xp_ceiling[self.level - 1]
            return (self.xp - ceiling_last_lvl) / (self.xp_ceiling[self.level] - ceiling_last_lvl)

    def getChargeThisTurn(self):
        """Returns the amount that the reactor will charge this turn"""
        try:
            return self.inventory.equipped['reactor'].getRechargeThisTurn()

        except AttributeError:
            return 0

    @property
    def image(self):
        try:
            if self.inventory.equipped['armor'].image is not Images.missing_image:
                self.base_image.blit(self.inventory.equipped['armor'].image, (0, 0))
        except AttributeError:
            # Player does not have armor equipped
            pass

        return self.base_image

    @image.setter
    def image(self, image):
        """Setting the players image actually sets a base image attribute"""
        self.base_image = image


class Item(Entity):
    """Represents entities which can be inside of an Inventory

    Child of Entity

    Attributes:


    Methods:
        drop(self) : Item is moved from inventory to floor
        pickUp(self) : Item is moved from floor to specified Inventory
    """
    image_dir = "Items"
    draw_order = DRAW_ORDER['ITEM']

    def __init__(self, item_id, data, location, x, y):

        self.id = item_id
        self.name = data['name']
        self.image_name = data['image']
        self.difficulty = data['difficulty']

        super().__init__(location, x, y)

    def drop(self):
        """Item is moved from inventory to floor"""
        # Unequip if equipped
        if self in self.location.equipped.values():
            self.unequip()

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

    @staticmethod
    def createItem(item_id, location, x=None, y=None):
        """Creates an item based on the type of ID"""
        # Everything before the underscore is the item class
        split_id = item_id.rsplit("_")
        item_class = split_id[0]

        if item_class == "BATTERY":
            item = Battery(item_id, location, x, y)
        elif item_class == "ARMOR":
            item = Armor(item_id, location, x, y)
        elif item_class in ("SWORD", "CLUB", "KNIFE", "PDW", "CANNON", "RIFLE", "PISTOL"):
            item = Weapon(item_id, location, x, y)
        elif item_class in ("QUICK", "BRAWLER", "FEEDER", "RANGER"):
            item = Reactor(item_id, location, x, y)
        else:
            raise ValueError("%s not recognized as a valid item class" % item_class)

        return item


class Weapon(Item):
    """Damage dealing item which can be equipped

    Child of Item, Entity

    """
    def __init__(self, item_id, location, x=None, y=None):
        self.item_class = 'weapon'

        data = Data.getItem("WEAPONS", item_id)

        self.melee_verb = data['melee_verb']
        self.melee_damage = data['melee_damage']
        self.melee_speed = data['melee_speed']
        self.is_quick_draw = data['quick_draw']
        self.is_ranged = bool(data['ranged'])
        if self.is_ranged:
            self.ranged_verb = data['ranged']['verb']
            self.ranged_damage = data['ranged']['damage']
            self.energy_per_shot = data['ranged']['energy']
            self.fire_rate = data['ranged']['fire_rate']
            self.range = data['ranged']['range']
            self.projectile = data['ranged']['projectile']

        super().__init__(item_id, data, location, x, y)

    def equip(self):
        self.location.equipped['weapon'] = self

    def unequip(self):
        self.location.equipped['weapon'] = None


class Armor(Item):
    """Item which provides defense when equipped

    Child of Item, Entity


    """
    def __init__(self, item_id, location, x=None, y=None):
        self.item_class = 'armor'
        data = Data.getItem("ARMOR", item_id)

        self.defense = data['defense']

        super().__init__(item_id, data, location, x, y)

    def equip(self):
        self.location.equipped['armor'] = self

    def unequip(self):
        self.location.equipped['armor'] = None


class Reactor(Item):
    """Item which provides energy when equipped

    Child of Item, Entity
    
    Attributes:
        max_charge : int
        recharge_rate : float
        recovery_time : int
        recoil_charge : float
        difficulty : int
        hit_this_turn : bool
        recovered : int : This will normally be at zero unless the charge is 0. 
            If the charge is at zero and hit_this_turn is False, increments by 1 until it reaches recovery time
            If hit while recovering, recovered resets to 0
            Reactor will not recharge until recovered
        current_charge : float
    """

    def __init__(self, item_id, location, x=None, y=None):
        self.item_class = 'reactor'
        data = Data.getItem("REACTORS", item_id)

        self.max_charge = data['max_charge']
        self.recharge_rate = data['recharge_rate']
        self.recovery_time = data['recovery']
        self.recoil_charge = data['recoil_charge']

        self.hit_this_turn = False
        self.recovered = 0

        # Current Charge Starts at 0
        self.current_charge = 0.0

        super().__init__(item_id, data, location, x, y)

    def equip(self):
        """Puts the reactor in the equipped reactor slot and reduces the current charge to 0"""
        self.location.equipped['reactor'] = self
        self.current_charge = 0.0

    def unequip(self):
        self.location.equipped['reactor'] = None

    def recharge(self):
        """Recovers or recharges the Reactor. Should be called once per turn
        
        If the reactor was not hit this turn and has not been completely depleted, recharges by the recharge rate amount
        After recharging, it ensures that current_charge does not exceed max_charge
        
        If the reactor was not hit this turn and is depleted, increases the recovered counter.
        If the recovered counter reached the recovery time, recharge by the recharge rate amount
        
        If was hit this turn, reset recovered counter
        """
        # Happens once per turn while equipped if not hit this turn
        if not self.hit_this_turn:
            if self.current_charge == 0:
                if self.recovered < self.recovery_time:
                    # If the reactor has not recovered yet, return
                    self.recovered += 1
                    return
                else:
                    # Reset the recovery clock and let recharge
                    self.recovered = 0

            new_charge_level = self.current_charge + self.recharge_rate
            if new_charge_level > self.max_charge:
                self.current_charge = self.max_charge
            else:
                self.current_charge = new_charge_level
        
        else:
            self.recovered = 0

    def rechargeToFull(self):
        """Sets the current charge to be equal to the max charge"""
        self.current_charge = self.max_charge

    def getRechargeThisTurn(self):
        """Used for printing to the information pane"""
        if self.hit_this_turn:
            return 0
        elif self.current_charge == 0 and self.recovered < self.recovery_time:
            return 0
        else:
            return self.recharge_rate


class Battery(Item):
    """Item which can be used to charge energy

    Child of Item, Entity


    """

    def __init__(self, item_id, location, x=None, y=None):
        """Extends the Entity init method"""
        self.item_class = "battery"

        data = Data.getItem("BATTERIES", item_id)
        self.power = data['power']

        super().__init__(item_id, data, location, x, y)

    def use(self):
        """Uses the battery, which increases the amount of charge in the reactor"""
        target = self.location.equipped['reactor']
        target.current_charge += self.power
        self.location.removeEntity(self)
