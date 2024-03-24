from datetime import date

from measurement.measures import Mass, Volume
from measurement.utils import guess

from mlcc.defaults import DEFAULT_SEPARATOR, ROUNDING_DECIMALS_IN_FLOAT
from mlcc.meal_type import MealType
from mlcc.unit_type import UnitType


def input_str(msg: str) -> str:
    while True:
        result = input(msg)
        if DEFAULT_SEPARATOR in result:
            print(f"Please do not use \"{DEFAULT_SEPARATOR}\"")
            continue
        return result


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


def is_quantity_valid(quantity: float, unit_type: UnitType, unit_symbol: str) -> bool:
    if unit_type != UnitType.NONE:
        if unit_type == UnitType.MASS:
            measure = Mass
        elif unit_type == UnitType.VOLUME:
            measure = Volume
        else:
            return False

        try:
            guess(quantity, unit_symbol, measures=[measure])
        except ValueError:
            return False

    return True


def guess_quantity(quantity: float, unit_type: UnitType, unit_symbol: str) -> str:
    if is_quantity_valid(quantity, unit_type, unit_symbol):
        if unit_type == UnitType.NONE:
            return f"{quantity} {unit_symbol}"
        else:
            if unit_type == UnitType.MASS:
                measure = Mass
            elif unit_type == UnitType.VOLUME:
                measure = Volume
            else:
                raise ValueError
            return str(guess(quantity, unit_symbol, measures=[measure]))
    else:
        return "<Invalid quantity>"


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
