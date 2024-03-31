from datetime import date
from typing import Optional

from mlcc.clients.text_input import input_date


class AbstractClientImplementation:

    def __init__(self) -> None:
        self.current_date = date.today()
        self.current_meal_name: Optional[str] = None
        self.current_food_name: Optional[str] = None

    def add_food_data(self) -> None:
        raise NotImplementedError

    def set_current_date(self) -> None:
        self.current_date = input_date()

    def display_food_data(self) -> None:
        raise NotImplementedError

    def display_food(self) -> None:
        raise NotImplementedError

    def set_current_food(self) -> None:
        raise NotImplementedError

    def get_current_food_name(self) -> str:
        return self.current_food_name

    def display_user_data(self) -> None:
        raise NotImplementedError

    def display_meals_of_the_day(self) -> None:
        raise NotImplementedError

    def set_current_meal(self) -> None:
        raise NotImplementedError

    def get_current_meal_name(self) -> str:
        return self.current_meal_name

    def display_current_meal(self) -> None:
        raise NotImplementedError

    def add_current_food_to_current_meal(self):
        raise NotImplementedError

    def save(self) -> None:
        raise NotImplementedError

    @staticmethod
    def exit() -> None:
        raise NotImplementedError
