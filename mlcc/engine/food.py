from typing import List

from mlcc.common import is_quantity_valid, guess_quantity
from mlcc.types.unit_type import UnitType


class Food:

    def __init__(self, name: str, calories: float, quantity: float, unit_type: UnitType, unit_symbol):
        self.name = name
        self.calories = calories
        self.quantity = quantity
        self.unit_type = unit_type
        self.unit_symbol = unit_symbol
        self.valid = self.is_valid()

    def __str__(self):
        guessed_quantity = guess_quantity(self.quantity, self.unit_type, self.unit_symbol)
        return (f"{self.calories} calories in {guessed_quantity} of {self.name} "
                f"({self.unit_type.name.lower()}/{'valid' if self.is_valid() else 'invalid'})")

    def __repr__(self):
        return f"{self.name=}, {self.calories=}, {self.quantity=}, {self.unit_type=}, {self.unit_symbol=}"

    def get_name(self) -> str:
        return self.name

    def serializable_list(self) -> List[str]:
        return [str(self.calories), str(self.quantity), str(self.unit_type.value), self.unit_symbol]

    def is_valid(self) -> bool:
        if self.name == "" or self.calories < 0 or self.quantity <= 0 or self.unit_symbol == "":
            return False
        else:
            return is_quantity_valid(self.quantity, self.unit_type, self.unit_symbol)
