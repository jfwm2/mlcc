from typing import Dict, List, Union

from mlcc.common.common import guess_quantity, is_quantity_valid
from mlcc.types.unit_type import UnitType


class Quantity:

    def __init__(self, value: float, unit_type: UnitType, unit_symbol: str) -> None:
        self.value = value
        self.unit_type = unit_type
        self.unit_symbol = unit_symbol

    def __str__(self):
        return f"{self.guessed()} ({self.unit_type.get_name().lower()}/{'valid' if self.is_valid() else 'invalid'})"

    def __repr__(self):
        return f"{self.value=}, {self.unit_type=}, {self.unit_symbol=}"

    def get_value(self) -> float:
        return self.value

    def get_unit_type(self) -> UnitType:
        return self.unit_type

    def get_unit_symbol(self) -> str:
        return self.unit_symbol

    def guessed(self) -> str:
        return guess_quantity(self.value, self.unit_type, self.unit_symbol)

    def is_valid(self) -> bool:
        return is_quantity_valid(self.value, self.unit_type, self.unit_symbol)

    def serializable_list(self) -> List[str]:
        return [str(self.value), str(self.unit_type.get_value()), self.unit_symbol]

    def get_serializable_dict(self) -> Dict[str, Union[float, int, str]]:
        return {'value': self.value, 'unit_type': self.unit_type.get_value(), 'unit_symbol': self.unit_symbol}
