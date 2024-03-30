from datetime import date

from mlcc.common.defaults import ROUNDING_DECIMALS_IN_FLOAT
from mlcc.common.trie_node import TrieNode
from mlcc.types.meal_type import MealType
from mlcc.types.unit_type import UnitType


def input_string(msg: str) -> str:
    return input(msg)


def input_float(msg: str) -> float:
    result = None
    while result is None:
        input_data = input(msg)
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


def input_string_with_trie(msg: str, trie: TrieNode) -> str:
    print(f"{msg} - {trie.get_next_chars()}")

    return ""
