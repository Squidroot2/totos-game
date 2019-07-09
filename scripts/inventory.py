class Inventory:
    ''' Component Class'''
    def __init__(self, owner, contents = []):
        self.owner = owner
        self.contents = contents
        self.equipped = {"weapon": None, "armor": None, "generator": None}
    
    def addEntity(self, item):
        self.contents.append(item)
        
    def removeEntity(self, item):
        self.contents.remove(item)
        