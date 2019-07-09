'''
Contains the classes used to construct actors(player,enemies,items)
'''
from scripts.constants import *
import os, pygame, random

# my modules
from scripts.inventory import *
from scripts.inventory import *

class Entity():
    image = pygame.image.load(os.path.join('images', 'unknown.png'))
    
    # todo Turn components into a dictionary,
    # todo rearrange signature so that map is first and is called location
    def __init__(self,x,y,map,components=[]):
        self.x = x
        self.y = y
        self.map = map
        self.map.addEntity(self)
        obstruct=False

        if 'AI' in components:
            self.ai = AI(self)
        else:
            self.ai = None
        
        if 'Inventory' in components:
            self.inventory = Inventory(self, components['Inventory'])
        else:
            self.inventory = None

    def draw(self, surface):
        surface.blit(self.image, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))

# todo move characters to seperate modules
class Character(Entity):

    dead = False
    
    # todo add ids for enemy types
    def __init__(self,x,y,map,components=[]):
        
        super().__init__(x,y,map,components)
        obstruct = True
        

    def move(self, delta_x, delta_y):
        destination = ((self.x+delta_x), (self.y+delta_y))
        if self.validateMove(destination):
            if not self.attack(destination):
                self.x += delta_x
                self.y += delta_y

    def validateMove(self, destination):
        # If destination is out of range
        if destination[0] < 0 or destination[0] >= self.map.width:
            return False
        elif destination[1] < 0 or destination[1] >= self.map.height:
            return False
        # If destination is blocked
        elif self.map.tile_map[destination[0]][destination[1]].block_path:
            return False
        else:
            return True

    def attack(self, destination):
        for entity in self.map.entities:
            if entity is self:
                continue
            elif (entity.x, entity.y) == destination:
                entity.kill()
                print("ATTACK")
                return True
        return False        

    def kill(self):
        self.dead = True
        self.ai = None
        self.map.removeEntity(self)
        # Create a corpse
        Corpse(self)
        
        
        
class Player(Character):
    image = pygame.image.load(os.path.join('images','characters','player.png'))
    
    def __init__(self,x,y,map,components={"Inventory": []}):
        
        super().__init__(x,y,map,components)
        
    def getStartingInventory(self):
    
        # Create Initial Items in Inventory
        gun = Weapon("HANDGUN1",self.inventory)
        knife = Weapon("KNIFE1",self.inventory)
        armor = Armor("ARMOR1",self.inventory)
        generator = Generator("LIGHT1", self.inventory)
        # Player starts with 2 batteries
        for i in range(2):
            Battery("TINY", self.inventory)
        
        # Equip Items
        gun.equip()
        armor.equip()
        generator.equip()
        
class Enemy(Character):
    image = pygame.image.load(os.path.join('images','characters','enemy.png'))

class Corpse(Entity):
    def __init__(self, character):
        if character.inventory:
            inventory_contents = character.inventory.contents
        else:
            inventory_contents = []
        super().__init__(character.x, character.y, character.map, components={'Inventory': inventory_contents})
        
    # todo add image for corpse
    
    


# todo seperate to seperate module
class AI:
    '''Component Class'''
    def __init__(self, owner):
        self.owner = owner

    def takeTurn(self):
        self.randomMove()

    def randomMove(self):
        x_move = random.randint(-1,1)
        y_move = random.randint(-1,1)
        self.owner.move(x_move, y_move)




