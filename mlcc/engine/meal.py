from typing import Dict

from mlcc.engine.food import Food
from mlcc.types.meal_type import MealType


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

    def add_food(self, food: Food, quantity_to_add: float) -> None:
        self.menu[food] = self.menu.get(food, 0.0) + quantity_to_add

    def get_calories_in_meal(self) -> float:
        return sum([quantity_in_menu * food.get_nutrition_data().get_calories_per_unit() for
                    food, quantity_in_menu in self.menu.items()])

    def get_quantity_in_meal(self, food: Food) -> float:
        return self.menu.get(food, 0.0)

    def serializable_dict(self) -> Dict[str, float]:
        return {food.name: quantity_in_menu for food, quantity_in_menu in self.menu.items()}
