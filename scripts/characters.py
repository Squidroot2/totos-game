from scripts.items import Weapon, Armor, Generator, Battery
from scripts.entities import Entity, Corpse
import pygame
import os

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

    def attack(self, destination):
        for entity in self.location.entities:
            if entity is self:
                continue
            elif entity.x == destination[0] and entity.y == destination[1]:
                entity.kill()
                print("ATTACK")
                return True
        return False

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
        
        
class Player(Character):
    image = pygame.image.load(os.path.join('images','characters','player.png'))
    
    def __init__(self,x,y,map,components={"Inventory": []}):
        
        super().__init__(x,y,map,components)
        level = 1
        xp = 0
        base_damage = 1
        base_defense = 0
        
    def setStartingInventory(self):
    
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
        
        # Shield Starts charged
        generator.rechargeToFull()
        
class Enemy(Character):
    image = pygame.image.load(os.path.join('images','characters','enemy.png'))