from objects.entities import Entity
import os
from scripts.utilities import getItemById

ITEM_JSON = os.path.join('data','items.json')

class Item(Entity):
    #todo finish Item docstrings
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
        
        
