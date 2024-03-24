from mlcc.meal import Meal
from mlcc.meal_type import MealType


class MealsOfTheDay:

    def __init__(self) -> None:
        self.meals = {meal_type: Meal() for meal_type in MealType}

    def select_meal(self) -> Meal:
        print("NOT IMPLEMENTED")
        pass
