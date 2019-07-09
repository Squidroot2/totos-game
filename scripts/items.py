from scripts.entities import Entity
import os
from scripts.utilities import readINI
from copy import copy

WEAPON_INI = os.path.join('data','weapons.ini')
ARMOR_INI = os.path.join('data','armor.ini')
GENERATOR_INI = os.path.join('data','generator.ini')
BATTERY_INI = os.path.join('data','battery.ini')

#todo write items classes
class Item(Entity):

    def __init__(self, location, x=None, y=None):
        # Location will be a floor or a container
        self.location = location
        self.x = x
        self.y = y
        self.location.addEntity(self)

    def drop(self):
        self.location.removeEntity(self)
        self.x = self.owner.x
        self.y = self.owner.y
        self.owner.floor.addEntity(item)
    
    def pickUp(self, inventory):
        self.location.removeEntity(self)
        self.x = None
        self.y = None
        inventory.addEntity(self)        
        
        
class Weapon(Item):
    
    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)
        
        config = readINI(WEAPON_INI)
        self.name =             config[item_id].get('name')
        self.melee_damage =     config[item_id].getint('melee_damage')
        self.is_quick_draw =    config[item_id].getboolean('quick_draw')
        self.fire_rate =        config[item_id].getint('fire_rate')
        self.difficulty =       config[item_id].getint('difficulty')
        self.is_ranged =        config[item_id].getboolean('is_ranged')
        if self.is_ranged:
            self.ranged_damage = config[item_id].getint('ranged_damage')
            self.energy_per_shot = config[item_id].getint('energy_per_shot')
        

    def equip(self):
        self.location.equipped['weapon'] = self
    

class Armor(Item):
    
    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)
        
        config = readINI(ARMOR_INI)
        self.name =         config[item_id].get('name')
        self.defense =      config[item_id].getint('defense')
        self.difficulty =   config[item_id].getint('difficulty')
    
    def equip(self):
        self.location.equipped['armor'] = self
    

class Generator(Item):

    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)
    
        config = readINI(GENERATOR_INI)
        self.name =             config[item_id].get('name')
        self.max_charge =       config[item_id].getint('max_charge')
        self.recharge_rate =    config[item_id].getfloat('recharge_rate')
        
        # Current Charge Starts at 0
        self.current_charge = 0.0
    
    def equip(self):
        self.location.equipped['generator'] = self
        self.current_charge = 0.0
        
    def recharge(self):
        # Happens once per turn while equipped
        new_charge_level = self.current_charge + self.recharge_rate
        if new_charge_level > self.max_charge:
            self.current_charge = self.max_charge
        else:
            self.current_charge = new_charge_level
    
    def rechargeToFull(self):
        self.current_charge = self.max_charge
        
    
class Battery(Item):
    
    def __init__(self, item_id, location, x=None, y=None):
        super().__init__(location, x, y)
        
        config = readINI(BATTERY_INI)
        self.name = config[item_id].get('name')
        self.power = config[item_id].getint('power')
    
    def use(self):
        target = self.location.equipped['generator']
        target.current_charge += self.power
        
        
