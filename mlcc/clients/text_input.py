from datetime import date
from typing import Dict

from mlcc.common.defaults import ROUNDING_DECIMALS_IN_FLOAT
from mlcc.common.trie import Trie
from mlcc.types.meal_type import MealType
from mlcc.types.unit_type import UnitType


def input_string(msg: str) -> str:
    return input(f"{msg}: ")


def input_float(msg: str) -> float:
    result = None
    while result is None:
        input_data = input(f"{msg}: ")
        try:
            result = float(input_data)
        except ValueError:
            print(f'Invalid entry; a float was expected, instead got {input_data}')
    return round(result, ROUNDING_DECIMALS_IN_FLOAT)


def input_unit_type() -> UnitType:
    msg = ""
    for idx, element in enumerate(UnitType):
        msg += f'{element.name.capitalize()}({idx}) '
    result = len(UnitType)
    while result < 0 or result >= len(UnitType):
        input_data = input(f"{msg}Unit type: ")
        try:
            result = int(input_data)
        except ValueError:
            print(f'Invalid entry; a integer was expected, instead got {input_data}')
            continue
        if result < 0 or result >= len(UnitType):
            print(f'Invalid entry; value should be between 0 and {len(UnitType) - 1}')
    return list(UnitType)[result]


def input_meal_type() -> MealType:
    msg = ""
    for idx, element in enumerate(MealType):
        msg += f'{element.name.capitalize()}({idx}) '
    result = len(MealType)
    while result < 0 or result >= len(MealType):
        input_data = input(f"{msg}Meal type: ")
        try:
            result = int(input_data)
        except ValueError:
            print(f'Invalid entry; a integer was expected, instead got {input_data}')
            continue
        if result < 0 or result >= len(MealType):
            print(f'Invalid entry; value should be between 0 and {len(MealType) - 1}')
    return list(MealType)[result]


def input_date() -> date:
    while True:
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        try:
            year, month, day = map(int, date_entry.split('-'))
            result = date(year, month, day)
        except ValueError:
            print(f"Invalid format {date_entry}")
            continue
        return result


def input_string_with_trie(msg: str, trie: Trie) -> str:
    result = ''
    while True:
        next_chars = trie.get_next_chars(result)
        if len(next_chars) == 0:
            break
        result_is_word = trie.is_word(result)
        s = input_string(f"{msg} "
                         f"[{'|'.join([result + '(' + word[0] + ')' + word[1:] for word in next_chars.values()])}]"
                         f"{f' (enter nothing to chose {result})' if result_is_word else ''}")
        if s in next_chars:
            result += next_chars[s]
        elif s.swapcase() in next_chars:
            result += next_chars[s.swapcase()]
        elif s == '' and result_is_word:
            break
        else:
            print("Invalid choice; select of one of the following characters "
                  f"{', '.join(next_chars.keys())}{' or nothing' if result_is_word else ''}")
    return result


def input_ad_hoc_type(type_dict: Dict[int, str], type_name: str) -> int:
    msg = ""
    for idx, element in type_dict.items():
        msg += f'{element.capitalize()}({idx}) '
    result = len(type_dict)
    while result not in type_dict.keys():
        input_data = input_string(f"{msg}{type_name} type")
        try:
            result = int(input_data)
        except ValueError:
            print(f'Invalid entry; a integer was expected, instead got {input_data}')
            continue
        if result not in type_dict.keys():
            print(f'Invalid entry; value should be within {list(type_dict.keys())}')
    return result
