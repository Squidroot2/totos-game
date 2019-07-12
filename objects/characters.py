from objects.items import Weapon, Armor, Generator, Battery
from objects.entities import Entity, Corpse
from scripts.utilities import readINI
from scripts import formulas
import pygame
import os, random

CHARACTER_INI = os.path.join('data','characters.ini')

class Character(Entity):

    dead = False
    
    # todo  finish using the characters ini to initialize character stats
    def __init__(self, char_id, floor, x, y, components=[]):

        config = readINI(CHARACTER_INI)

        if config[char_id].getboolean('has_inventory'):
            components = {'Inventory': []}
        # todo use the inventory type

        super().__init__(floor, x, y, components)

        self.name =     config[char_id].get('name')
        self.level =    config[char_id].getint('level')
        self.xp =       config[char_id].getint('xp')
        self.life =     config[char_id].getint('life')
        self.base_damage = config[char_id].getint('damage')
        self.base_defense = config[char_id].getint('defense')
        self.base_attack_rate = config[char_id].getint('attack_rate')

        image_name = config[char_id].get('image')
        self.image = pygame.image.load(os.path.join('images', 'characters', image_name)).convert_alpha()

        self.obstruct = True

    def move(self, delta_x, delta_y):
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            if not self.checkEntityObstruct(destination):
                self.x += delta_x
                self.y += delta_y

    def validateMove(self, destination):
        # If destination is out of range
        if destination[0] < 0 or destination[0] >= self.location.width:
            print("Invalid move X")
            return False
        elif destination[1] < 0 or destination[1] >= self.location.height:
            print("invalid move Y")
            return False
        # If destination is blocked
        elif not self.location.map.walkable[destination[1]][destination[0]]:
            print("Invalid move, blocked")
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

        damage = formulas.getDamageDealt(attack, defense)

        self_enc = self.getEncumbrance()
        enemy_enc = opponent.getEncumbrance()
        hit_chance = formulas.getHitChance(self_enc, enemy_enc)


        for attack in range(self.getAttackRate()):

            roll = random.random()
            if roll < hit_chance:
                print(self.name + " hit " + opponent.name + " for " + str(damage) + " damage")
                opponent.takeDamage(damage)


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
                print(self.name + " energy depleted")
        else:
            damage_to_flesh = damage

        killed = formulas.determineLethal(damage_to_flesh, self.life)

        if killed:
            self.kill()
        else:
            injured = formulas.determineInjury(damage_to_flesh, self.life)
            if injured:
                print(self.name + " injured")
                self.life -= 1

    def kill(self):
        self.dead = True
        self.ai = None
        self.location.removeEntity(self)
        # Create a corpse
        Corpse(self)
    
    def getDefense(self):
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

        # Find out if carrying weapon; if not, return base_attack_rate
        if self.inventory and self.inventory.equipped['weapon']:
            weapon = self.inventory.equipped['weapon']
        else:
            return self.base_attack_rate

        #
        if not ranged:
            return weapon.melee_speed
        else:
            return weapon.fire_rate

    def getEncumbrance(self):
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



        
class Player(Character):
    image = pygame.image.load(os.path.join('images','characters','player.png'))
    
    def __init__(self,map,x,y,components={"Inventory": []}):
        
        super().__init__("PLAYER",map,x,y,components)
        self.level = 1
        self.xp = 0
        self.base_damage = 1
        self.base_defense = 0
        self.base_attack_rate = 1
        self.setStartingInventory()


    # todo move inventory stuff to inventory class with ids
    def setStartingInventory(self):
    
        # Create Initial Items in Inventory
        gun = Weapon("HANDGUN1", self.inventory)
        armor = Armor("ARMOR1", self.inventory)
        generator = Generator("LIGHT1", self.inventory)
        Weapon("KNIFE1", self.inventory)

        # Player starts with 2 batteries
        for i in range(2):
            Battery("TINY", self.inventory)
        
        # Equip Items
        gun.equip()
        armor.equip()
        generator.equip()
        
        # Shield Starts charged
        generator.rechargeToFull()

# todo figure out if I want to have an enemy class
# class Enemy(Character):
#     image = pygame.image.load(os.path.join('images', 'characters', 'enemy.png'))
#     obstruct = True