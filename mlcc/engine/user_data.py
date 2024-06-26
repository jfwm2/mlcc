import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Union

from mlcc.common.common import get_date_from_string
from mlcc.engine.food_data import FoodData
from mlcc.engine.meals_of_the_day import MealsOfTheDay
from mlcc.types.meal_type import MealType


class UserData:
    def __init__(self, user_data_file: Path, food_data: FoodData) -> None:
        self.user_data_file = user_data_file
        self.data: Dict[date, MealsOfTheDay] = {}
        self.load_data(food_data)

    def __str__(self) -> str:
        return f"User data; content: {len(self.data)} dates"

    def load_data(self, food_data: FoodData) -> None:
        print(f'Loading user data from {self.user_data_file}')
        val_to_meal_type = {val.value: val for val in MealType}
        serialized_data: Dict[str, Dict[str, Dict[str, float]]] = json.loads(self.user_data_file.read_text())
        for day_date, day_meals in serialized_data.items():
            meals_date = get_date_from_string(day_date)
            self.data[meals_date] = MealsOfTheDay(meals_date)
            for meal_type_val, meal_dict in day_meals.items():
                meal = self.data[meals_date].select_meal(val_to_meal_type[int(meal_type_val)])
                for food_name, quantity in meal_dict.items():
                    meal.add_food(food_data.get_food_by_name(food_name), quantity)

    def get_or_create_meals_of_the_day(self, meals_date: date) -> MealsOfTheDay:
        if meals_date not in self.data:
            self.data[meals_date] = MealsOfTheDay(meals_date)
        return self.get_meals_of_the_day(meals_date)

    def get_all_dates(self) -> List[date]:
        return list(self.data.keys())

    def get_meals_of_the_day(self, d: date) -> Optional[MealsOfTheDay]:
        return self.data.get(d, None)

    def save(self) -> None:
        serializable_data = \
            {str(meal_date): meals_of_the_day.serializable_dict() for meal_date, meals_of_the_day in self.data.items()}
        print(f'Saving user data to {self.user_data_file}')
        with open(self.user_data_file, "w") as outfile:
            json.dump(serializable_data, outfile)

    def get_serializable_dict(self) -> Dict[
        str, Union[str, Dict[str, Union[float, str, Dict[int, Dict[str, Union[int, float, str, Dict[str, float]]]]]]]]:
        return {
            'meals_per_day': {str(meal_date): meals_of_the_day.get_serializable_dict() for meal_date, meals_of_the_day
                              in self.data.items()},
            'description': str(self),
            'type': str(self.__class__.__name__)
        }
