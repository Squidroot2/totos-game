import random


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