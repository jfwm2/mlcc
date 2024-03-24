import json

from enum import Enum
from measurement.measures import Mass, Volume
from measurement.utils import guess
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_DATA_DIR = '~/.mlcc/data'
FOOD_DATA_FILE = 'food_data.json'
USER_DATA_FILE = 'user_data.json'
DATA_FILES = [FOOD_DATA_FILE, USER_DATA_FILE]
ROUNDING_DECIMALS_IN_FLOAT = 2


class UnitType(Enum):
    NONE = 0
    MASS = 1
    VOLUME = 2


def input_float(msg: str) -> float:
    result = None
    while result is None:
        input_str = input(msg)
        try:
            result = float(input_str)
        except ValueError:
            print(f'Invalid entry; a float was expected, instead got {input_str}')
    return round(result, ROUNDING_DECIMALS_IN_FLOAT)


def input_unit_type() -> UnitType:
    msg = ""
    for idx, element in enumerate(UnitType):
        msg += f'{element.name.capitalize()}({idx}) '
    result = len(UnitType)
    while result < 0 or result >= len(UnitType):
        input_str = input(f"{msg}Unit type: ")
        try:
            result = int(input_str)
        except ValueError:
            print(f'Invalid entry; a integer was expected, instead got {input_str}')
        if result < 0 or result >= len(UnitType):
            print(f'Invalid entry; value should be between 0 and {len(UnitType) - 1}')
    return list(UnitType)[result]


def is_quantity_valid(quantity: float, unit_type: UnitType, unit_symbol: str) -> bool:
    if unit_type != UnitType.NONE:
        if unit_type == UnitType.MASS:
            measure = Mass
        elif unit_type == UnitType.VOLUME:
            measure = Volume
        else:
            return False

        try:
            guess(quantity, unit_symbol, measures=[measure])
        except ValueError:
            return False

    return True


def guess_quantity(quantity: float, unit_type: UnitType, unit_symbol: str) -> str:
    if is_quantity_valid(quantity, unit_type, unit_symbol):
        if unit_type == UnitType.NONE:
            return f"{quantity} {unit_symbol}"
        else:
            if unit_type == UnitType.MASS:
                measure = Mass
            elif unit_type == UnitType.VOLUME:
                measure = Volume
            else:
                raise ValueError
            return str(guess(quantity, unit_symbol, measures=[measure]))
    else:
        return "<Invalid quantity>"


class MyLittleCalorieCounter:
    @staticmethod
    def _create_data_files_if_not_exist(data_dir_path: Path) -> None:
        print(f'Checking data dir {data_dir_path}')
        if not data_dir_path.exists():
            print(f'Creating data dir {data_dir_path}')
            data_dir_path.mkdir(parents=True)

        for data_file in DATA_FILES:
            print(f'Checking data file {data_file}')
            data_file_path = data_dir_path / data_file
            if not data_file_path.exists():
                print(f'Creating empty data file {data_file_path}')

    def __init__(self, data_dir=DEFAULT_DATA_DIR) -> None:
        data_dir_path: Path = Path(data_dir).expanduser().resolve()
        MyLittleCalorieCounter._create_data_files_if_not_exist(data_dir_path)
        self.food_data = FoodData(data_dir_path / FOOD_DATA_FILE)
        self.repl()

    def repl(self) -> None:
        input_str = ''
        while input_str.upper() != 'X':
            input_str = input("(A)dd or (D)isplay foods / (S)ave / e(X)it -- Input: ")
            if input_str.upper() not in 'ADSX':
                print(f'Invalid input {input_str}')
            elif input_str.upper() == 'A':
                self.food_data.add()
            elif input_str.upper() == 'D':
                self.food_data.display()
            elif input_str.upper() == 'S':
                self.food_data.save()
            else:
                print("Exiting")


class FoodData:
    def __init__(self, food_data_file: Path) -> None:
        self.food_data_file = food_data_file
        self.data: Dict[str, Food] = {}
        self.load_data()

    def load_data(self) -> None:
        print(f'Loading food data from {self.food_data_file}')
        val_to_unit_type = {val.value: val for val in UnitType}
        serialized_data: dict[str, str] = json.loads(self.food_data_file.read_text())
        for name, serialized_food in serialized_data.items():
            food_elements = serialized_food.split('|')
            assert len(food_elements) == 4
            self.data[name] = Food(name=name, calories=float(food_elements[0]), quantity=float(food_elements[1]),
                                   unit_type=val_to_unit_type[int(food_elements[2])], unit_symbol=food_elements[3])

    def add(self) -> None:
        name = input("New food name: ")

        if name in self.data:
            print('food name is already present, please choose another one')

        quantity = 0
        unit_type = UnitType.NONE
        unit_symbol = ''
        valid_quantity = False
        while not valid_quantity:
            quantity = input_float(f"Quantity of {name}: ")
            unit_type = input_unit_type()
            unit_symbol = input("Unit symbol: ")
            valid_quantity = is_quantity_valid(quantity, unit_type, unit_symbol)
            if not valid_quantity:
                print(f"the quantity entered for food {name}; {quantity} {unit_symbol} "
                      f"({unit_type.name.lower()}) is not valid")

        guessed_quantity = guess_quantity(quantity, unit_type, unit_symbol)
        calories = input_float(f"Calories in {guessed_quantity} of {name}: ")

        food = Food(name=name, calories=calories, quantity=quantity, unit_type=unit_type, unit_symbol=unit_symbol)
        self.data[name] = food
        print(f"{food} entered")

    def display(self) -> None:
        for name, food in self.data.items():
            print(f"{name}: {food}")

    def save(self) -> None:
        serialized_data = {name: food.serialize() for name, food in self.data.items()}
        print(f'Savin food data to {self.food_data_file}')
        with open(self.food_data_file, "w") as outfile:
            json.dump(serialized_data, outfile)


class Food:

    def __init__(self, name: str, calories: float, quantity: float, unit_type: UnitType, unit_symbol):
        self.name = name
        self.calories = calories
        self.quantity = quantity
        self.unit_type = unit_type
        self.unit_symbol = unit_symbol
        self.valid = self.is_valid()

    def __str__(self):
        guessed_quantity = guess_quantity(self.quantity, self.unit_type, self.unit_symbol)
        return (f"{self.calories} calories in {guessed_quantity} of {self.name} "
                f"({self.unit_type.name.lower()}/{'valid' if self.is_valid() else 'invalid'})")

    def __repr__(self):
        return f"{self.name=}, {self.calories=}, {self.quantity=}, {self.unit_type=}, {self.unit_symbol=}"

    def serialize(self) -> str:
        return f"{self.calories}|{self.quantity}|{self.unit_type.value}|{self.unit_symbol}"

    def is_valid(self) -> bool:
        if self.name == "" or self.calories < 0 or self.quantity <= 0 or self.unit_symbol == "":
            return False
        else:
            return is_quantity_valid(self.quantity, self.unit_type, self.unit_symbol)
