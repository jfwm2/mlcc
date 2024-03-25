import json
from pathlib import Path
from typing import Dict, Optional

from mlcc.common import input_string, input_float, input_unit_type, is_quantity_valid, guess_quantity
from mlcc.defaults import DEFAULT_SEPARATOR
from mlcc.food import Food
from mlcc.unit_type import UnitType


class FoodData:
    def __init__(self, food_data_file: Path) -> None:
        self.food_data_file = food_data_file
        self.data: Dict[str, Food] = {}
        self.load_data()

    def load_data(self) -> None:
        print(f'Loading food data from {self.food_data_file}')
        val_to_unit_type = {val.value: val for val in UnitType}
        serialized_data: Dict[str, str] = json.loads(self.food_data_file.read_text())
        for name, serialized_food in serialized_data.items():
            food_elements = serialized_food.split(DEFAULT_SEPARATOR)
            assert len(food_elements) == 4
            self.data[name] = Food(name=name, calories=float(food_elements[0]), quantity=float(food_elements[1]),
                                   unit_type=val_to_unit_type[int(food_elements[2])], unit_symbol=food_elements[3])

    def add(self) -> None:
        name = input_string("New food name: ")

        if name in self.data:
            print('food name is already present, please choose another one')
        else:
            quantity = 0
            unit_type = UnitType.NONE
            unit_symbol = ''
            valid_quantity = False
            while not valid_quantity:
                quantity = input_float(f"Quantity of {name}: ")
                unit_type = input_unit_type()
                unit_symbol = input_string("Unit symbol: ")
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
        print(f'Saving food data to {self.food_data_file}')
        with open(self.food_data_file, "w") as outfile:
            json.dump(serialized_data, outfile)

    def select_food(self, name: str) -> Optional[Food]:
        return self.data.get(name, None)
