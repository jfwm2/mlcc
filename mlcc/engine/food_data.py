import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from mlcc.engine.food import Food
from mlcc.types.unit_type import UnitType


class FoodData:
    def __init__(self, food_data_file: Path) -> None:
        self.food_data_file = food_data_file
        self.data: Dict[str, Food] = {}
        self.load_data()

    def __str__(self) -> str:
        return f"Food data; content: {len(self.data)} foods"

    def load_data(self) -> None:
        print(f'Loading food data from {self.food_data_file}')
        val_to_unit_type = {val.value: val for val in UnitType}
        serialized_data: Dict[str, str] = json.loads(self.food_data_file.read_text())
        for name, food_elements in serialized_data.items():
            assert len(food_elements) == 4
            self.add(name=name, calories=float(food_elements[0]), quantity=float(food_elements[1]),
                     unit_type=val_to_unit_type[int(food_elements[2])], unit_symbol=food_elements[3])

    def add(self, name: str, calories: float, quantity: float, unit_type: UnitType, unit_symbol: str) -> None:
        food = Food(name=name, calories=calories, quantity=quantity, unit_type=unit_type, unit_symbol=unit_symbol)
        self.data[name] = food

    def save(self) -> None:
        serialized_data = {name: food.get_nutrition_data().serializable_list() for name, food in self.data.items()}
        print(f'Saving food data to {self.food_data_file}')
        with open(self.food_data_file, "w") as outfile:
            json.dump(serialized_data, outfile)

    def get_food_by_name(self, name: str) -> Optional[Food]:
        return self.data.get(name, None)

    def get_all_food_names(self) -> List[str]:
        return list(self.data.keys())

    def exists(self, name: str) -> bool:
        return name in self.data

    def get_serializable_dict(self) -> Dict[
        str, Union[str, List[Dict[str, Union[str, Dict[str, Union[float, str, Dict[str, Union[float, int, str]]]]]]]]]:
        return {
            'data': [food.get_serializable_dict() for food in self.data.values()],
            'description': str(self),
            'type': str(self.__class__.__name__)
        }
