from typing import Dict

from mlcc.engine.meal import Meal
from mlcc.types.meal_type import MealType


class MealsOfTheDay:

    def __init__(self) -> None:
        self.meals = {meal_type: Meal(meal_type) for meal_type in MealType}

    def __str__(self) -> str:
        return str({k.name: v for k, v in self.meals.items()})

    def __repr__(self) -> str:
        return str(self)

    def select_meal(self, meal_type: MealType) -> Meal:
        return self.meals[meal_type]

    def display(self) -> None:
        for meal in self.meals.values():
            meal.display()

    def calories(self) -> float:
        return sum([meal.calories() for meal in self.meals.values()])

    def serializable_dict(self) -> Dict[int, Dict[str, float]]:
        return {meal_type.value: meal.serializable_dict() for meal_type, meal in self.meals.items()}
