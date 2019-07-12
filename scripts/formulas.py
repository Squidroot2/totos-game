import math
import random

def getHitChance(attacker_enc,defender_enc):
    return .9 - (attacker_enc * .15) + (defender_enc * .1)


def getDamageDealt(attack, defense):

    # Uses a logarithmic function to find damage reduction.
    # Attack is fed into Log Base so that higher damage means lower reduction
    reduction = math.log(defense/20+1, attack+1)*3

    damage = attack - attack*reduction

    # Damage is rounded to nearest tenth
    return round(damage,1)

def determineLethal(damage, life):
    """Returns whether the damage to flesh killed the character or not"""
    if life <= 0:
        return True
    chance = damage/life

    roll = random.random()

    if roll < chance:
        return True
    else:
        return False

def determineInjury(damage, life):
    """Returns whether the damage to flesh has inflicted an injury which will reduce the life points"""

    chance = damage*2/life

    roll = random.random()

    if roll < chance:
        return True
    else:
        return False