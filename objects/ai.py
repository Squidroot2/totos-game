import random

class AI:
    """Component Class for Characters
    
    Attributes:
        owner : Character
        type : string in ("basic","brainless")
        opponent : Player or None: Stores the player here when it is found
    
    Methods:
        findPlayer(self) : Searches through the list of entites in the location to find the player
        takeTurn(self) : Runs through conditional statements to determine how the AI will act this turn
        moveNextToEntity(self, target) : 
        randomMove(self) : Moves randomly no more than 1 tile
    """
    def __init__(self, owner, ai_type):
        self.owner = owner
        assert ai_type in ("basic", "brainless")
        self.type = ai_type
        self.opponent = None

    # todo figure out a way to identify the player as the opponent
    def findPlayer(self):
        """Searches through the list of entities in the location to find the player"""
        for entity in self.owner.location.entities:
            if entity.is_player:
                return entity
        return None

    def takeTurn(self):
        """Runs through conitional statements to determine how the AI will act this turn"""
        if self.opponent is None:
            self.opponent = self.findPlayer()
        
        # If the entity is not discovered move around peacefully
        if not self.owner.discovered:
            self.randomMove(peacefully=True)

        # Otherwise, move based on ai type
        else:
            # Brainless AI
            if self.type == "brainless":
                self.randomMove()

            # Basic AI decisions
            if self.type == "basic":
                if self.owner.location is self.opponent.location:
                    self.moveNextToEntity(self.opponent)

                # If the ai owner is on a different floor
                else:
                    self.randomMove(peacefully=True)

    # todo write method for moving the ai's entity towards the player or other entity
    def moveNextToEntity(self, target):
        pass


    def randomMove(self, peacefully=False):
        """Choose a random x and y movement. Could be (0,0)
        
        Parameters:
            peacefully : bool : passed to the Character.move() method
        """
        x_move = random.randint(-1, 1)
        y_move = random.randint(-1, 1)
        self.owner.move(x_move, y_move, peacefully)

