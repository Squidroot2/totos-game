def getHitChance(attacker_enc,defender_enc):
    return .9 - (attacker_enc * .15) + (defender_enc * .1)