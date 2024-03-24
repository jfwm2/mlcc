from measurement.measures import Mass, Volume
from measurement.utils import guess

from mlcc.defaults import ROUNDING_DECIMALS_IN_FLOAT
from mlcc.unit_type import UnitType


def input_float(msg: str) -> float:
    result = None
    while result is None:
        input_str = input(msg)
        try:
            result = float(input_str)
        except ValueError:
            print(f'Invalid entry; a float was expected, instead got {input_str}')
    return round(result, ROUNDING_DECIMALS_IN_FLOAT)


def input_unit_type() -> UnitType:
    msg = ""
    for idx, element in enumerate(UnitType):
        msg += f'{element.name.capitalize()}({idx}) '
    result = len(UnitType)
    while result < 0 or result >= len(UnitType):
        input_str = input(f"{msg}Unit type: ")
        try:
            result = int(input_str)
        except ValueError:
            print(f'Invalid entry; a integer was expected, instead got {input_str}')
        if result < 0 or result >= len(UnitType):
            print(f'Invalid entry; value should be between 0 and {len(UnitType) - 1}')
    return list(UnitType)[result]


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
