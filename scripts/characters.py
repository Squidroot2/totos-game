from scripts.items import Weapon, Armor, Generator, Battery
from scripts.entities import Entity, Corpse
from scripts.utilities import readINI
from scripts import formulas
import pygame
import os

CHARACTER_INI = os.path.join('data','characters.ini')

class Character(Entity):

    dead = False
    
    # todo  finish using the characters ini to initialize character stats
    def __init__(self,char_id, map,x,y,components=[]):

        config = readINI(CHARACTER_INI)

        if config[char_id].getboolean('has_inventory'):
            components = {'Inventory': []}
        # todo get inventory in here

        super().__init__(map,x,y,components)

        self.name =     config[char_id].get('name')
        self.level =    config[char_id].getint('level')
        self.xp =       config[char_id].getint('xp')
        self.base_damage = config[char_id].getint('damage')
        self.base_defense = config[char_id].getint('defense')
        self.base_attack_rate = config[char_id].getint('attack_rate')

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
                print("ATTACK")
                return True
        return False

    #todo finish function
    def meleeAttack(self, enemy):
        damage = self.getMeleeDamage()
        damage -= enemy.getDefense()

        self_enc = self.getEncumbrance()
        enemy_enc = enemy.getEncumbrance()
        hit_chance = formulas.getHitChance(self_enc,enemy_enc)


        for attack in range(self.getFireRate()):
            pass


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
            return 0
        else:
            equipment = self.inventory.equipped
            for item in equipment:
                if equipment[item] is not None and equipment[item].difficulty > self.level:
                    encumbrance += equipment[item].difficulty - self.level
    #todo finish getEnergy()
    def getEnergy(self):
        pass



        
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