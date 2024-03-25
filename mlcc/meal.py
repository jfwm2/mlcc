from typing import Dict

from mlcc.food import Food
from mlcc.meal_type import MealType


class Meal:

    def __init__(self, type: MealType) -> None:
        self.type = type
        self.menu: Dict[Food, float] = {}

    def __str__(self) -> str:
        return str({k.name: v for k, v in self.menu.items()})

    def __repr__(self) -> str:
        return str(self)

    def get_type(self) -> MealType:
        return self.type

    def add_food(self, food: Food, quantity: float, display: bool = True) -> None:
        new_quantity = self.menu.get(food, 0.0) + quantity
        self.menu[food] = new_quantity
        if display:
            print(f"{quantity} {food.unit_symbol} {food.name} added to {self.type.name.lower()}; "
                  f"total {new_quantity} {food.unit_symbol} -> {quantity * food.calories / food.quantity:2f} cal")

    def calories(self) -> float:
        return sum([quantity * food.calories / food.quantity for food, quantity in self.menu.items()])

    def display(self):
        print(f"{self.type.name.capitalize()}:",
              ','.join([f"{quantity} {food.unit_symbol} of {food.name}" for food, quantity in self.menu.items()]),
              f'total of {self.calories():2f} calories')

    def serializable_dict(self) -> Dict[str, float]:
        return {food.name: quantity for food, quantity in self.menu.items()}
