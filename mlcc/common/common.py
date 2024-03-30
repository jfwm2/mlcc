from measurement.measures import Mass, Volume
from measurement.utils import guess

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
