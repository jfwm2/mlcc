from datetime import date
from typing import Optional

from measurement.measures import Mass, Volume
from measurement.utils import guess

from mlcc.types.meal_type import MealType
from mlcc.types.unit_type import UnitType


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


def get_meal_type_by_name(name: str) -> Optional[MealType]:
    for t in MealType:
        if t.get_name().upper() == name.upper():
            return t
    return None


def get_meal_type_by_value(value: int) -> Optional[MealType]:
    for t in MealType:
        if t.get_value() == value:
            return t
    return None


def get_date_from_string(date_str: str) -> Optional[date]:
    try:
        year, month, day = map(int, date_str.split('-'))
        return date(year, month, day)
    except SyntaxError:
        return None
    except ValueError:
        return None
