""" Contains formulas that are used during combat 

Functions:

....getHitChance(attacker_enc, defender_enc)
....getDamaageDealt(attack, defense)
....determineLethal(damage, life)
....determineInjury(damage, life)
"""
# Standard Library
import math
import random
RANGE_BASE_HIT_CHANCE = 1
RANGE_EXCEEDED_PENALTY = -0.3
RANGE_ENCUMBRANCE_PENALTY = -0.25

def getMeleeHitChance(attacker_enc, defender_enc):
    """ Takes the attackers encumbrance and the defender's encumbrance and returns a floating number between 0 and 1 representing the chance to hit the defender

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
    """Returns a float 0-1 that indicates the chance of a ranged attack landing"""
    
    # Base chance to hit
    base = RANGE_BASE_HIT_CHANCE
    
    # Calculate Penalties
    enc_penalty = attacker_enc * RANGE_ENCUMBRANCE_PENALTY
    range_penalty = range_exceeded * RANGE_EXCEEDED_PENALTY
    
    # Calculate Bonus
    enc_bonus = defender_enc * .1
    
    # Return sum of base, penalities, and bonus
    return math.fsum([base, enc_penalty, range_penalty, enc_bonus])

def getMaxRange(encumbrance, peak_range):
    """Given the encumbrance and rated range, returns the range at which, any further and the chance to hit would be 0"""
    return math.floor((((-RANGE_ENCUMBRANCE_PENALTY * encumbrance) - RANGE_BASE_HIT_CHANCE) / RANGE_EXCEEDED_PENALTY) + peak_range)


def getDamageDealt(attack, defense):
    """Determines the damage dealt using the attacker's raw attack damage and the defender's defense
    
    Parameters:
        attack: float or int
        defense; float or int
    
    Returns:
        : float : Rounded to the first decimal place
    
    Calls:
        math.log(x, base)
    """
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