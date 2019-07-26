""" Contains formulas that are used during combat 

Functions:

....getHitChance(attacker_enc, defender_enc)
....getDamaageDealt(attack, defense)
....determineLethal(damage, life)
....determineInjury(damage, life)
"""

import math
import random


def getMeleeHitChance(attacker_enc, defender_enc):
    """ Takes the attackers encumbrance and the defender's encumbrance and returns a floating number between representing the chance to hit the defender

    Values 0 and lower represent 0 chance while 1 and above is guaranteed chance"""
    # Base chance to hit
    base = 1
    
    # Calculate Penalty
    enc_penalty = attacker_enc * -0.1
    
    # Calculate Bonus
    enc_bonus = defender_enc * 0.1
        
    # Return sum of base, penalty and bonus
    return math.fsum([base,enc_penalty, enc_bonus])
    

def getRangedHitChance(attacker_enc, defender_enc, range_exceeded):
    # Base chance to hit
    base = .95
    
    # Calculate Penalties
    enc_penalty = attacker_enc * -0.15
    range_penalty = range_exceeded * -0.15
    
    # Calculate Bonus
    enc_bonus = defender_enc * .1
    
    # Return sum of base, penalities, and bonus
    return math.fsum([base, enc_penalty, range_penalty, enc_bonus])


def getDamageDealt(attack, defense):
    """Determines the damage dealt using the attacker's raw attack damage and the defender's defense"""
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