import json

from pathlib import Path
from typing import Dict

from mlcc.common import input_float, input_unit_type, is_quantity_valid, guess_quantity
from mlcc.food import Food
from mlcc.unit_type import UnitType


class UserData:
    def __init__(self, user_data_file: Path) -> None:
        self.user_data_file = user_data_file
        self.data: Dict[str, MealsOfTheDay] = {}
        self.load_data()

    def load_data(self) -> None:
        print(f'Loading user data from {self.user_data_file}')

    def add(self) -> None:
        print("NOT IMPLEMENTED")

    def display(self) -> None:
        print("NOT IMPLEMENTED")

    def save(self) -> None:
        print("NOT IMPLEMENTED")


class MealsOfTheDay:

    def __init__(self) -> None:
        pass

