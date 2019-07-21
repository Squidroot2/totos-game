import random


class AI:
    """Component Class"""
    def __init__(self, owner, ai_type):
        self.owner = owner
        assert ai_type in ("basic", "brainless")
        self.type = ai_type

    def takeTurn(self):
        if self.type == "brainless":
            self.randomMove()

    def randomMove(self):
        x_move = random.randint(-1, 1)
        y_move = random.randint(-1, 1)
        self.owner.move(x_move, y_move)
