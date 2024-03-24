from typing import Dict

from mlcc.food import Food
from mlcc.meal_type import MealType


class Meal:

    def __init__(self, type: MealType) -> None:
        self.type = type
        self.menu: Dict[Food, int] = {}

    def get_type(self) -> MealType:
        return self.type

    def add_food(self, food: Food) -> None:
        print("NOT IMPLEMENTED")
