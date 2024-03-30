from mlcc.engine.nutrition_data import NutritionData
from mlcc.types.unit_type import UnitType


class Food:

    def __init__(self, name: str, calories: float, quantity: float, unit_type: UnitType, unit_symbol):
        self.name = name
        self.nutrition_data = NutritionData(calories=calories, quantity=quantity,
                                            unit_type=unit_type, unit_symbol=unit_symbol)

    def __str__(self):
        return (f"{self.nutrition_data.get_calories()} calories in {self.nutrition_data.get_quantity().guessed()} of "
                f"{self.name} ({self.nutrition_data.get_quantity().unit_type.get_name().lower()}/"
                f"{'valid' if self.is_valid() else 'invalid'})")

    def __repr__(self):
        return f"{self.name=}, {self.nutrition_data=}"

    def get_name(self) -> str:
        return self.name

    def get_nutrition_data(self) -> NutritionData:
        return self.nutrition_data

    def is_valid(self) -> bool:
        if self.name == "":
            return False
        else:
            return self.nutrition_data.is_valid()
