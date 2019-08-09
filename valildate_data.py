"""Validates the information contained in the JSON files in the Data Folder"""
from source.utilities import loadJson
from json.decoder import JSONDecodeError

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
        print("Error in Character JSON")
        print()
        validation_failed = True
    
    # Items JSON file
    valid = validateItems()
    if not valid:
        print("Error in Items JSON")
        print()
        validation_failed = True
    
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
    
    try:
        for char_id in data:
            char = data[char_id]
            assert(type(char['name']) == str or char['name'] is None)
            assert(type(char['image']) == str)
            assert(type(char['verb']) == str)
            assert(type(char['level']) == int)
            assert(type(char['xp']) == int)
            assert(type(char['life']) == int)
            assert(type(char['damage']) in (int, float))
            assert(type(char['defense']) in (int, float))
            assert(type(char['attack_rate']) == int)
            assert(type(char['innate_ranged']) == dict or char['innate_ranged'] is None)
            if char['innate_ranged']:
                assert(type(char['innate_ranged']['verb']) == str)
                assert(type(char['innate_ranged']['damage']) in (int,float))
                assert(type(char['innate_ranged']['range']) == int)
                assert(type(char['innate_ranged']['rate']) == int)
                assert(type(char['innate_ranged']['rate']) == int)
                assert(type(char['innate_ranged']['projectile']) == str)
            assert(type(char['ai']) == str or char['ai'] is None)
            assert(type(char['inventory']) == str or char['inventory'] is None)
        
        return True
    
    except KeyError as e:
        print("Missing key %s in %s Character" %(e, char_id))
        return False
   
    except AssertionError:
        print("Invalid Type for variable in %s" % char_id)
        return False


def validateItems():
    """Validate Items File"""
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
        print("Missing Category %s in %s" %(e, items_json))
        return False
    
    # Validate Battery Names
    try:
        for battery in  batteries:
            id_parts = battery.split("_")
            assert(id_parts[0] == "BATTERY")
            
    except AssertionError:
        print("Invalid Battery name %s" %battery)
        return False
    
    return True
if __name__ == '__main__':
    main()