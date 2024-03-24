from datetime import date
from pathlib import Path
from typing import Dict

from mlcc.meals_of_the_day import MealsOfTheDay


class UserData:
    def __init__(self, user_data_file: Path) -> None:
        self.user_data_file = user_data_file
        self.data: Dict[date, MealsOfTheDay] = {}
        self.load_data()

    def load_data(self) -> None:
        print(f'Loading user data from {self.user_data_file}')

    def get_or_create_meals_of_the_day(self, meals_date: date) -> MealsOfTheDay:
        if meals_date not in self.data:
            self.data[meals_date] = MealsOfTheDay()
        return self.data[meals_date]

    def add(self) -> None:
        print("NOT IMPLEMENTED")

    def display(self) -> None:
        print("NOT IMPLEMENTED")

    def save(self) -> None:
        print("NOT IMPLEMENTED")
