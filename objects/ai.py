import random

class AI:
    """Component Class"""
    def __init__(self, owner, ai_type):
        self.owner = owner
        assert ai_type in ("basic", "brainless")
        self.type = ai_type
        self.opponent = None

    # todo figure out a way to identify the player as the opponent
    def findPlayer(self):
        """Searches through the list of entities in the location"""
        for entity in self.owner.location.entities:
            if entity.is_player:
                return entity
        return None

    def takeTurn(self):
        if self.opponent is None:
            self.opponent = self.findPlayer()
        # If the entity is not discovered move around peacefully
        if not self.owner.discovered:
            self.randomMove(peacefully=True)

        # Otherwise, move based on ai type
        else:
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
        x_move = random.randint(-1, 1)
        y_move = random.randint(-1, 1)
        self.owner.move(x_move, y_move, peacefully)

