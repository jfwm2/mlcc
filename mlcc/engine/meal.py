from typing import Dict, Union

from mlcc.engine.food import Food
from mlcc.types.meal_type import MealType


class Meal:

    def __init__(self, meal_type: MealType) -> None:
        self.type = meal_type
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

    def get_serializable_dict(self) -> Dict[str, Union[int, float, str, Dict[str, float]]]:
        return {
            'meal_type': self.type.get_value(),
            'menu': {food.get_name(): amount for food, amount in self.menu.items()},
            "calories": self.get_calories_in_meal(),
            'description': str(self),
            'type': str(self.__class__.__name__)
        }
