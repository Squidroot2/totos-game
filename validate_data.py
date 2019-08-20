"""Validates the information contained in the JSON files in the Data Folder"""
from source.utilities import loadJson
from source.constants import WEAPONS, REACTORS
from json.decoder import JSONDecodeError
from voluptuous import Schema, Any, Maybe, In
import voluptuous.error
import os.path

data_folder = 'data'

characters_json = os.path.join(data_folder, 'characters.json')
items_json = os.path.join(data_folder, 'items.json')
leveled_lists_json = os.path.join(data_folder, 'leveled_lists.json')
inventories_json = os.path.join(data_folder, 'inventories.json')

def main():
    """First confirm all files are present and can be loaded,
    Then load and verify Items and put items into items list
    Then load and verify inventory using items list and put inventories into inventory list
    Then load and verify characters using inventory list and put characters into character list
    Finally load and verify leveled_lists using characters and items lists"""
    
    print()
    print("Validating Files... \n")
    
    validation_succeeded = runValidation()
    
    # Print Success if there were not failures
    if validation_succeeded:
        print("Validation Completed Successfully!")
    else:
        print("Validation Failed")
    input()

def runValidation():
    """Runs all validation
    
    Returns: bool
    """
    
    
    # Files are present
    valid = validatePresent()
    if not valid:
        print("Error: Missing File(s) \n")
        return False
   
    # Items JSON file
    valid, item_names = validateItems()
    if not valid:
        print("Error in %s \n" % items_json)
        return False

    
    valid, inventory_list = validateInventories(item_names)
    if not valid:
        print("Error in %s \n" % inventories_json)
        return False

    # Characters JSON file
    valid, character_names = validateCharacters(inventory_list)
    if not valid:
        print("Error(s) in %s \n" % characters_json)
        return False

    # todo validate leveled_lists JSONs
    valid = validateLeveledList(item_names, character_names)
    if not valid:
        print("Error(s) in %s \n" % leveled_lists_json)
        return False

    print()
    
    return True

def validatePresent():
    """Determines if the files are present"""
    assert(os.path.exists(characters_json))
    assert(os.path.exists(items_json))
    assert(os.path.exists(leveled_lists_json))
    assert(os.path.exists(inventories_json))
    
    return True
    
        
def validateCharacters(inventory_list):
    """Validate the characters json

    Returns: bool, list
    """
    try:
        data = loadJson(characters_json)
    except JSONDecodeError:
        print("Error loading %s" %characters_json)
        return False, []
    
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
        'ai': Maybe(str),
        'inventory': Maybe(In(inventory_list))
    }, required=True)

    names = []
    try:
        for char_id in data:
            names.append(char_id)
            char_schema(data[char_id])
    except voluptuous.error.Invalid as e:
        print("Error with Character %s: %s" % (char_id, e))
        return False, names

    return True, names


def validateItems():
    """Validate Items File

    Returns : bool"""

    valid = True

    # Validate File can be loaded
    try:
        data = loadJson(items_json)
    except JSONDecodeError:
        print("Error loading %s" %items_json)
        return False, []

    # Get the Categories of items
    try:
        armors = data['ARMOR']
        weapons = data['WEAPONS']
        reactors = data['REACTORS']
        batteries = data['BATTERIES']
    except KeyError as e:
        print("Missing Category %s in %s" % (e, items_json))
        return False, []

    # Schemas
    
    armor_schema = Schema({
        'name': str,
        'image': Maybe(str),
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
        'image': Maybe(str),
        'power': Any(int, float),
        'difficulty': int
    }, required=True)

    item_names = []
    # Validate Batteries
    for battery in batteries:
        item_names.append(battery)
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
        item_names.append(armor)
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
        item_names.append(weapon)
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
        item_names.append(reactor)
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
            
    return valid, item_names


def validateInventories(item_names):
    """Validates the inventories JSON
    
    returns : bool, list
    """
    valid = True
    try:
        data = loadJson(inventories_json)
    except JSONDecodeError:
        print("Error loading %s" % items_json)
        return False, []
    
    inventory_list = []
    
    inventory_schema = Schema({
        "weapon": Maybe(In(item_names)),
        "armor": Maybe(In(item_names)),
        "reactor": Maybe(In(item_names)),
        "other": Maybe([In(item_names)])
        }, required=True)

    for inventory_type in data:
        inventory_list.append(inventory_type)
        for inventory in data[inventory_type]:
            try:
                inventory_schema(data[inventory_type][inventory])
            except voluptuous.error.Invalid as e:
                print("Error with inventory type %s, %s: %s" %(inventory_type, inventory, e))
                valid = False
        
        
    return valid, inventory_list


def validateLeveledList(item_names, character_names):
    #todo
    valid = True

    # Attempt Loading File
    try:
        data = loadJson(leveled_lists_json)
    except JSONDecodeError:
        print("Error loading %s" % leveled_lists_json)
        return False

    # Main Schema
    main_schema = Schema({
        'ENEMIES': dict,
        'ITEMS': dict,
        'CONSUMABLES': dict
    }, required=True)
    # Validate main schema
    try:
        main_schema(data)
    except voluptuous.error.Invalid as e:
        print("Error with structure of %s: %s" % (leveled_lists_json, e))
        return False

    # Item Leveled List Schema
    items_schema = Schema({
        In(item_names): int
    })

    # Validate Item Schema
    for item_list in data["ITEMS"]:
        try:
            items_schema(data["ITEMS"][item_list])
        except voluptuous.error.Invalid as e:
            print("Error in Item Leveled List %s: %s" % (item_list, e))
            valid = False

    # Enemy Leveled List Schema
    items_schema = Schema({
        In(character_names): int
    })

    # Validate Enemy Schema
    for enemy_list in data["ENEMIES"]:
        try:
            items_schema(data["ENEMIES"][enemy_list])
        except voluptuous.error.Invalid as e:
            print("Error in Item Leveled List %s: %s" % (enemy_list, e))
            valid = False

    # Consumable Leveled List Schema
    consum_schema = Schema({
        In(item_names): int
    })
    
    # Validate Consumables Schema
    for consum_list in data["CONSUMABLES"]:
        try:
            consum_schema(data["CONSUMABLES"][consum_list])
        except voluptuous.error.Invalid as e:
            print("Error in Consumable Leveled List %s: %s" % (consum_list, e))
            valid = False
        if sum(data["CONSUMABLES"][consum_list].values()) != 100:
            print("Warning: Consumables %s list sum does not equal 100" % consum_list)
    
    return valid


if __name__ == '__main__':
    main()