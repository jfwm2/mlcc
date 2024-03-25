from datetime import date
from pathlib import Path
from typing import Optional

from mlcc.common import input_date, input_meal_type, input_float, input_string
from mlcc.defaults import DEFAULT_DATA_DIR, FOOD_DATA_FILE, USER_DATA_FILE, DATA_FILES
from mlcc.food_data import FoodData
from mlcc.meals_of_the_day import Meal
from mlcc.user_data import UserData


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
        self.user_data = UserData(data_dir_path / USER_DATA_FILE, self.food_data)
        self.current_date = date.today()
        self.repl()

    def repl(self) -> None:
        input_str = ''
        current_meal: Optional[Meal] = None
        current_food: Optional[FOOD_DATA_FILE] = None
        while input_str.upper() != 'X':
            current_meal_str = '' if current_meal is None else f'[{current_meal.get_type().name.capitalize()}] '
            current_food_str = '' if current_food is None else f'[{current_food.get_name()}] '
            input_str = input(f"[{self.current_date}] (L)ist, (C)hange, or s(H)ow date / "
                              f"ch(O)ose of sho(W) meal {current_meal_str}/ "
                              f"add (F)ood to meal / (A)dd, l(I)st, (D)isplay or s(E)lect food {current_food_str}/ "
                              "(S)ave / e(X)it -- Input: ")
            if input_str.upper() not in 'LCHOWFAIDESX':
                print(f'Invalid input {input_str}')
            elif input_str.upper() == 'L':
                self.user_data.display()
            elif input_str.upper() == 'C':
                self.current_date = input_date()
            elif input_str.upper() == 'H':
                self.user_data.get_or_create_meals_of_the_day(self.current_date).display()
            elif input_str.upper() == 'O':
                current_meal = (
                    self.user_data.get_or_create_meals_of_the_day(self.current_date).select_meal(input_meal_type()))
            elif input_str.upper() == 'W':
                if current_meal is None:
                    print('No meal selected')
                    continue
                current_meal.display()
            elif input_str.upper() == 'F':
                if current_meal is None:
                    print('No meal selected')
                    continue
                if current_food is None:
                    print('No food selected')
                    continue
                quantity = (
                    input_float(f"How much {current_food.unit_symbol} of {current_food.name} would you like to add: "))
                current_meal.add_food(current_food, quantity)
            elif input_str.upper() == 'A':
                self.food_data.add()
            elif input_str.upper() == 'I':
                self.food_data.display()
            elif input_str.upper() == 'D':
                if current_food is None:
                    print('No food selected')
                    continue
                print(current_food)
            elif input_str.upper() == 'E':
                food_name = input_string("Name of the food to select: ")
                current_food = self.food_data.select_food(food_name)
            elif input_str.upper() == 'S':
                self.food_data.save()
                self.user_data.save()
            else:
                print("Exiting")
