from typing import List

from mlcc.engine.quantity import Quantity
from mlcc.types.unit_type import UnitType


class NutritionData:

    def __init__(self, calories: float, quantity: float, unit_type: UnitType, unit_symbol: str) -> None:
        self.calories = calories
        self.quantity = Quantity(quantity, unit_type, unit_symbol)

    def __str__(self) -> str:
        return (f"{self.calories} in {self.quantity.get_value()} {self.quantity.get_unit_symbol()} "
                f"({self.quantity.get_unit_type().get_name().lower()}/{'valid' if self.is_valid() else 'invalid'})")

    def __repr__(self):
        return f"{self.calories=}, {self.quantity=}"

    def is_valid(self) -> bool:
        if self.calories < 0:
            return False
        else:
            return self.quantity.is_valid()

    def get_calories(self) -> float:
        return self.calories

    def get_quantity(self) -> Quantity:
        return self.quantity

    def get_calories_per_unit(self) -> float:
        return self.calories / self.quantity.get_value()

    def serializable_list(self) -> List[str]:
        return [str(self.calories)] + self.quantity.serializable_list()
