from scripts.entities import Entity


#todo write items classes
class Item(Entity):

    def __init__(self, location, x=None, y=None):
        # Location will be a floor or a container
        self.location = location
        self.x = x
        self.y = y

class Weapon(Item):
    
    def __init__(self, name, location, x=None, y=None):
        super().__init__(location, x, y)
        self.name = name
    
    