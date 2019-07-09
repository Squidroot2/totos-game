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
    
    def __init__(self, name, level, location, x=None, y=None):
        super().__init__(location, x, y)
        self.name = name
        config = _readINI

    def _readINI(self):
        config = configparser.ConfigParser()
        config.read(WEAPON_INI)
        return config



    