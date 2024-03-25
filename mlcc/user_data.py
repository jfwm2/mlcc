import json
from datetime import date
from pathlib import Path
from typing import Dict

from mlcc.food_data import FoodData
from mlcc.meal_type import MealType
from mlcc.meals_of_the_day import MealsOfTheDay


class UserData:
    def __init__(self, user_data_file: Path, food_data: FoodData) -> None:
        self.user_data_file = user_data_file
        self.data: Dict[date, MealsOfTheDay] = {}
        self.load_data(food_data)

    def load_data(self, food_data: FoodData) -> None:
        print(f'Loading user data from {self.user_data_file}')
        val_to_meal_type = {val.value: val for val in MealType}
        serialized_data: Dict[str, Dict[str, Dict[str, float]]] = json.loads(self.user_data_file.read_text())
        for day_date, day_meals in serialized_data.items():
            year, month, day = map(int, day_date.split('-'))
            self.data[date(year, month, day)] = MealsOfTheDay()
            for meal_type_val, meal_dict in day_meals.items():
                meal = self.data[date(year, month, day)].select_meal(val_to_meal_type[int(meal_type_val)])
                for food_name, quantity in meal_dict.items():
                    meal.add_food(food_data.select_food(food_name), quantity, False)

    def get_or_create_meals_of_the_day(self, meals_date: date) -> MealsOfTheDay:
        if meals_date not in self.data:
            self.data[meals_date] = MealsOfTheDay()
        return self.data[meals_date]

    def display(self) -> None:
        for day_date, day_meals in self.data.items():
            print(f"{day_date} -- {day_meals.calories()} --")
            day_meals.display()

    def save(self) -> None:
        serializable_data = \
            {str(meal_date): meals_of_the_day.serializable_dict() for meal_date, meals_of_the_day in self.data.items()}
        print(f'Saving user data to {self.user_data_file}')
        with open(self.user_data_file, "w") as outfile:
            json.dump(serializable_data, outfile)
