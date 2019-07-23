from objects.entities import Entity, Corpse
from objects.game import Log
from scripts.utilities import getItemById
from scripts import formulas
import os, random

# Location of the json file which holds the character data
CHARACTER_JSON = os.path.join('data', 'characters.json')


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
            if not self.checkEntityObstruct(destination, peacefully):
                self.x += delta_x
                self.y += delta_y

    def validateMove(self, destination):
        """Returns True if the destination is walkable and False if it isn't"""
        # If destination is blocked
        if self.location.map.walkable[destination[1]][destination[0]]:
            return True
        else:
            return False

    def checkEntityObstruct(self, destination, peacefully):
        """Checks if an obstructing entity is in the destination. If it is, attack it.

        Parameters:
            destination : 2-tuple of ints : (x,y) format
            peacefully : boolean : If true, does not attack

         """
         # todo make it so this method merely returns the obstructing entity at this location
        for entity in self.location.entities:
            if entity is self or not entity.obstruct:
                continue
            elif entity.x == destination[0] and entity.y == destination[1]:
                if not peacefully:
                    self.meleeAttack(entity)
                return True
        return False

    def meleeAttack(self, opponent):
        """Attacks a specified opponent with a melee attack
        
        Parameters:
            opponent : Character
        """
        attack = self.getMeleeDamage()
        defense = opponent.getDefense()

        # Determines the damage based on the
        damage = formulas.getDamageDealt(attack, defense)

        # Gets the encumbrance of the two characters
        self_enc = self.getEncumbrance()
        enemy_enc = opponent.getEncumbrance()

        # Determines the hit chance based on the encumbrances
        hit_chance = formulas.getHitChance(self_enc, enemy_enc)

        # For every attack in the quantity of attack rate...
        for attack in range(self.getAttackRate()):
            # Roll to determine if attack landed
            roll = random.random()
            if roll < hit_chance:
                Log.addMessage(self.name + " hit " + opponent.name + " for " + str(damage) + " damage")
                opponent.takeDamage(damage)
        # Send a message if the opponent was killed
        if opponent.is_dead:
            Log.addMessage(self.name + " killed " + opponent.name)

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
                Log.addMessage(self.name + " energy depleted")
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
        """Gets the amount of melee damage that a character can deal per attack including weapon damage"""
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


