from mlcc.meal import Meal
from mlcc.meal_type import MealType


class MealsOfTheDay:

    def __init__(self) -> None:
        self.meals = {meal_type: Meal(meal_type) for meal_type in MealType}

    def select_meal(self, meal_type: MealType) -> Meal:
        return self.meals[meal_type]
