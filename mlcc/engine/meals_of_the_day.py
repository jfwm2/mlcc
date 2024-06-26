from datetime import date
from typing import Dict, Union

from mlcc.common.defaults import ROUNDING_DECIMALS_IN_FLOAT
from mlcc.engine.meal import Meal
from mlcc.types.meal_type import MealType


class MealsOfTheDay:

    def __init__(self, meals_date: date) -> None:
        self.meals_date = meals_date
        self.meals = {meal_type: Meal(meal_type) for meal_type in MealType}

    def __str__(self) -> str:
        return f"{self.meals_date} -- {round(self.get_calories(), ROUNDING_DECIMALS_IN_FLOAT)} calories"

    def __repr__(self) -> str:
        return str({k.name: v for k, v in self.meals.items()})

    def select_meal(self, meal_type: MealType) -> Meal:
        return self.meals[meal_type]

    def get_calories(self) -> float:
        return sum([meal.get_calories_in_meal() for meal in self.meals.values()])

    def get_meals(self) -> Dict[MealType, Meal]:
        return self.meals

    def get_meal(self, meal_type: MealType) -> Meal:
        return self.meals[meal_type]

    def serializable_dict(self) -> Dict[int, Dict[str, float]]:
        return {meal_type.get_value(): meal.serializable_dict() for meal_type, meal in self.meals.items()}

    def get_serializable_dict(self) -> Dict[
        str, Union[float, str, Dict[int, Dict[str, Union[int, float, str, Dict[str, float]]]]]]:
        return {
            'meals': {meal_type.get_value(): meal.get_serializable_dict() for meal_type, meal in self.meals.items()},
            'calories': self.get_calories(),
            'description': str(self),
            'type': str(self.__class__.__name__)
        }
