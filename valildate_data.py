"""Validates the information contained in the JSON files in the Data Folder"""
from source.utilities import loadJson
from source.constants import WEAPONS, REACTORS
from json.decoder import JSONDecodeError
from voluptuous import Schema, Any
import voluptuous.error
import os.path

data_folder = 'data'

characters_json = os.path.join(data_folder, 'characters.json')
items_json = os.path.join(data_folder, 'items.json')
leveled_lists_json = os.path.join(data_folder, 'leveled_lists.json')
inventories_json = os.path.join(data_folder, 'inventories.json')

def main():
    print()
    print("Validating Files...")
    print()
    
    validation_failed = False
    
    # Files are present
    valid = validatePresent()
    if not valid:
        print("Error: Missing File(s)")
        print()
        validation_failed = True
        
    # Characters JSON file
    valid = validateCharacters()
    if not valid:
        print("Error(s) in %s" % characters_json)
        print()
        validation_failed = True
    
    # Items JSON file
    valid = validateItems()
    if not valid:
        print("Error in %s" % items_json)
        print()
        validation_failed = True

    # todo validate inventories and leveled_lists JSONs
    
    # Print Success if there were not failures
    if not validation_failed:
        print("Validation Completed Successfully!")
    
    else:
        print("Validation Failed")
    input()

def validatePresent():
    """Determines if the files are present"""
    assert(os.path.exists(characters_json))
    assert(os.path.exists(items_json))
    assert(os.path.exists(leveled_lists_json))
    assert(os.path.exists(inventories_json))
    
    return True
    
        
def validateCharacters():
    """Validate the characters json"""
    try:
        data = loadJson(characters_json)
    except JSONDecodeError:
        print("Error loading %s" %characters_json)
        return False
    
    char_schema = Schema({
        'name': str,
        'image': str,
        'verb': str,
        'level': int,
        'xp': int,
        'life': int,
        'damage': Any(int, float),
        'defense': int,
        'attack_rate': int,
        'innate_ranged': Any(None, {
            'verb': str,
            'damage': Any(int, float),
            'range': int,
            'rate': int,
            'projectile': str
        }, required=True),
        'ai': Any(None, str),
        'inventory': Any(None, str)
    }, required=True)

    try:
        for char_id in data:
            char_schema(data[char_id])
    except voluptuous.error.Invalid as e:
        print("Error with Character %s: %s" % (char_id, e))
        return False

    return True


def validateItems():
    """Validate Items File

    Returns : bool"""

    valid = True

    # Validate File can be loaded
    try:
        data = loadJson(items_json)
    except JSONDecodeError:
        print("Error loading %s" %items_json)
        return False

    # Get the Categories of items
    try:
        armors = data['ARMOR']
        weapons = data['WEAPONS']
        reactors = data['REACTORS']
        batteries = data['BATTERIES']
    except KeyError as e:
        print("Missing Category %s in %s" % (e, items_json))
        return False

    # Schemas
    
    armor_schema = Schema({
        'name': str,
        'image': Any(None, str),
        'defense': int,
        'difficulty': int
    }, required=True)
    weapon_schema = Schema({
        'name': str,
        'image': Any(None, str),
        'melee_verb': str,
        'melee_damage': Any(int, float),
        'melee_speed': int,
        'quick_draw': bool,
        'difficulty': int,
        'ranged': Any(None, {
            'verb': str,
            'damage': Any(int, float),
            'energy': Any(int, float),
            'fire_rate': int,
            'range': int,
            'projectile': str
        }, required=True)
    }, required=True)
    reactor_schema = Schema({
        'name': str,
        'image': Any(None, str),
        'max_charge': int,
        'recharge_rate': float,
        'recovery': int,
        'recoil_charge': Any(int, float),
        'difficulty': int
    }, required=True)
    battery_schema = Schema({
        'name': str,
        'image': Any(None, str),
        'power': Any(int, float),
        'difficulty': int
    }, required=True)

    # Validate Batteries
    for battery in batteries:
        try:
            id_parts = battery.split("_")
            assert (id_parts[0] == "BATTERY")
            battery_schema(batteries[battery])
        except AssertionError:
            print("Invalid Battery name %s" % battery)
            valid = False
        except voluptuous.error.Invalid as e:
            print("Error with %s: %s" % (battery, e))
            valid = False

    # Validate Armors
    for armor in armors:
        try:
            id_parts = armor.split("_")
            assert (id_parts[0] == "ARMOR")
            armor_schema(armors[armor])
        except AssertionError:
            print("Invalid Armor name %s" % armor)
            valid = False
        except voluptuous.error.Invalid as e:
            print("Error with %s: %s" % (armor, e))
            valid = False

    # Validate Weapons
    for weapon in weapons:
        try:
            id_parts = weapon.split("_")
            assert (id_parts[0] in WEAPONS)
            weapon_schema(weapons[weapon])
        except AssertionError:
            print("Invalid Weapon name %s" % weapon)
            valid = False
        except voluptuous.error.Invalid as e:
            print("Error with %s: %s" % (weapon, e))
            valid = False

    # Validate Reactors
    for reactor in reactors:
        try:
            id_parts = reactor.split("_")
            assert (id_parts[0] in REACTORS)
            reactor_schema(reactors[reactor])
        except AssertionError:
            print("Invalid Reactor name %s" % reactor)
            valid = False
        except voluptuous.error.Invalid as e:
            print("Error with %s: %s" % (reactor, e))
            valid = False
    return valid


if __name__ == '__main__':
    main()