# Trial of the Outer Spiral
Trial of the Outer Spiral is a sci-fi themed [roguelike](https://en.wikipedia.org/wiki/Roguelike) game written in Python. This project is still a work in progress

## Requirements
  * Python 3
  * numpy
  * pygame
  * python-tcod
  * Microsoft Visual C++ Redistributable or GCC (for tcod)
  * voluptuous required to run validate_data.py
 

## How To Play
### Object of Game
The object of the Trial of the Outer Spiral is to get through all 100 floors of the randomly generated trial. Each floor is filled with Enemies 
which are trying to stop you. Run or fight is up to you but you must find the down portal on each floor in order to proceed. You will also find items along the floor which will help you on your journey. Items include weapons, 
armor, reactors, and batteries. If you should fall before reaching the end of the trial, you must start from the beginning.

### Combat
**Combat Basics**
Combat in TOTOS is turn-based and symmetrical. Turn-based, in that after every move the player makes, all of the enemies then make a move. Symmetrical, in that all statistics being equal(attack, defense, equipment etc) the player and enemies will do the same damage, use the same amount of energy, and have the same level of survivablity.

**Energy**
Unlike many games, characters have one bar which is spent when using certain attacks, and is depleted when taking damage.
Because of this, the energy bar should be thought of as both a "stamina bar" and a "health bar". Energy comes from a character's reactor. 
The reactor determines max capacity, recharge rate, recoil charge, and recovery time.
Each turn that a reactor does not take damage, it recharges by its recharge amount unless it is in recovery mode.
When an attack deals more damage than the amount of energy remaining in the reactor, the reactor's energy is depleted to zero. 
No matter how much the damage exceeds the energy remaining, no damage will happen to flesh so as long as the energy is not at zero.
A reactor enters recovery mode when it is depleted to zero. During recovery mode, the reactor will not naturally recharge. If a character is attacked during recovery mode, their recovery timer is reset.
When a reactor is first equipped, it starts in recovery mode with zero energy.
Each ranged weapon uses a certain amount of energy in order to shoot. If there is not enough energy, the weapon cannot be used for ranged attacks. 
Most reactors will recycle at least part of the energy used by a weapon back into the energy pool. The maximum amount that can be recycled back is called the recoil charge amount.
Melee attacks and innate ranged attacks, do not use energy and can be used even if energy is completely depleted. 

**Life**
When an attack hits a character with no energy, damage is dealt to flesh. Every attack to flesh has a chance of killing or injuring a character. 
The higher the amount of life, the higher the chance to survive a hit to flesh and to not receive an injury. If a character does suffer an injury, their life is reduced by 1, making them more vulnerable to future attacks

**Damage**
There are two main types of damage: ranged and melee. Both of these takes can either be weapon attacks or natural attacks. 
All weapons have melee damage. Using a weapon to deal melee damage ADDS to the character's natural damage. 
On the other hand, using a weapon to deal ranged damage REPLACES the character's  natural damage. Not all weapons have ranged capabilities in which case trying to use a ranged attack will use the character's natural ranged attack.

**Defense**
Defense reduces the amount of damage that is dealt. Defense affects attacks against both flesh and energy. 
Total defense is the character's natural defense plus any defense from the armor they are wearing.

**Fire Rate/ Attack Rate**
Characters can perform multiple attacks in a single turn against a single target. This is determined by innate ability OR if using a weapon, the weapons stats. In general, a low-damage/high rate is going to be better for low-defense opponents, while a high-damage/low-rate is going to be better against high-defense opponents.

**Accuracy**
By default, ranged attacks have an accuracy of 95% and melee attacks have an accuracy of 100%. There are a couple of facters that can modify this percentage. Namely, these are encumbrance and range which are explained below. Note that the accuracy displayed on the side panel only takes into account the player's encumbrance.

**Encumbrance**
Encumbrance is when a character uses an item that has a level above their own. This is done for every equipped item individually, not an average. 
For example, if a LVL 2 Character has a LVL 4 Weapon, LVL 1 Reactor, and LVL 2 Armor, the character has an encumbrance of 2. 
Every level encumbrance reduces the character's accuracy by 15 percentage points. On the flip side, the chance to hit is increased by 10 percentage points for every point of encumbrance that the defending character has.

**Range**
All ranged weapons have a range statistic which determines how far they can shoot while maintaining peak accuracy. Note that weapons can be aimed outside of this range so range should be thought of as "optimal range" rather than "maximum range". For every tile past the range, accuracy is reduced by 15 percentage points.

### The Player
**Background**
The game starts with the player choosing their name and background. There are 5 Choices:
* Officer: Starts with a quick-drawing Pistol and Nightstick, LVL 1 Armor, and a fast charging reactor
* Marksman: Starts with a Rifle, LVL 1 Armor, and a well-rounded reactor
* Agent: Starts with a 3-round burst PDW, LVL 1 Armor, and an efficient-recycler reactor
* Pointman: Starts with a Cannon, LVL 1 Armor, and a high-capacity reactor
* Gladiator: Starts with a Sword, LVL 2 Armor, and a brawler's reactor

**Experience**
Every time the player kills an enemy, they gain experience. After a certain amount of experience, the player levels up. 
Besides reducing the encumbrance from using higher-level equipment, leveling up also increases the player's stats

**Inventory**
In addition to the starting items, the player will also pick up items found throughout the game. The player's inventory has 10 slots to hold these items.

### Controls
**Main**
* Movement: Numpad 
* Wait: Numpad 5
* Rest : KeyPad 0
* Fire: F
* Pick Up: G
* Look Around: L
* Inventory : I

**Inventory**
* Select Item: 0-9
* Exit Inventory : ESC or I

**Fire Mode**
* Move Target: Numpad
* Fire: F
* Exit Fire Mode: ESC

## Compatibility
I have tested running the game on Fedora 29 and Windows 10. I expect it to run on any operating system

## Credits
Big thanks to the following

* TypodermicFonts (Unispace)

  
