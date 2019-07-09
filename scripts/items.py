from scripts.entities import Entity
import configparser, os

WEAPON_INI = os.path.join('data','weapons.ini')


#todo write items classes
class Item(Entity):

    def __init__(self, location, x=None, y=None):
        # Location will be a floor or a container
        self.location = location
        self.x = x
        self.y = y

class Weapon(Item):
    
    def __init__(self, id, location, x=None, y=None):
        super().__init__(location, x, y)
        config = _readINI
        self.name =             config[id].get('name')
        self.melee_damage =     config[id].getint('melee_damage')
        self.is_quick_draw =    config[id].getboolean('quick_draw')
        self.fire_rate =        config[id].getint('fire_rate')
        self.difficulty =       config[id].getint('difficulty')
        self.is_ranged =        config[id].getboolean('is_ranged')
        if self.is_ranged:
            self.ranged_damage = config[id].getint('ranged_damage')
            self.energy_per_shot = config[id].getint('energy_per_shot')
        

    def _readINI(self):
        config = configparser.ConfigParser()
        config.read(WEAPON_INI)
        return config

