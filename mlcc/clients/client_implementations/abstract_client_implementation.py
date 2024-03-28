from datetime import date
from typing import Optional

from mlcc.engine.food import Food
from mlcc.engine.meals_of_the_day import Meal


class AbstractClientImplementation:

    def __init__(self) -> None:
        self.current_date = date.today()
        self.current_meal: Optional[Meal] = None
        self.current_food: Optional[Food] = None

    def add_food_data(self) -> None:
        raise NotImplementedError

    def set_current_date(self) -> None:
        raise NotImplementedError

    def display_food_data(self) -> None:
        raise NotImplementedError

    def display_food(self) -> None:
        raise NotImplementedError

    def set_current_food(self) -> None:
        raise NotImplementedError

    def get_current_food_name(self) -> str:
        raise NotImplementedError

    def display_user_data(self) -> None:
        raise NotImplementedError

    def display_meals_of_the_day(self) -> None:
        raise NotImplementedError

    def set_current_meal(self) -> None:
        raise NotImplementedError

    def get_current_meal_name(self) -> str:
        raise NotImplementedError

    def display_current_meal(self) -> None:
        raise NotImplementedError

    def add_current_food_to_current_meal(self):
        raise NotImplementedError

    def save(self) -> None:
        raise NotImplementedError

    @staticmethod
    def exit() -> None:
        raise NotImplementedError
