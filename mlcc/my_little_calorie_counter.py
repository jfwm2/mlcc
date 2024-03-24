from datetime import date
from pathlib import Path

from mlcc.common import input_date
from mlcc.defaults import DEFAULT_DATA_DIR, FOOD_DATA_FILE, USER_DATA_FILE, DATA_FILES
from mlcc.food_data import FoodData
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
        self.user_data = UserData(data_dir_path / USER_DATA_FILE)
        self.current_date = date.today()
        self.repl()

    def repl(self) -> None:
        input_str = ''
        while input_str.upper() != 'X':
            input_str = input(f"[{self.current_date}] (C)hange date /"
                              " (A)dd or (D)isplay foods / (S)ave / e(X)it -- Input: ")
            if input_str.upper() not in 'CADSX':
                print(f'Invalid input {input_str}')
            elif input_str.upper() == 'C':
                self.current_date = input_date()
            elif input_str.upper() == 'A':
                self.food_data.add()
            elif input_str.upper() == 'D':
                self.food_data.display()
            elif input_str.upper() == 'S':
                self.food_data.save()
            else:
                print("Exiting")
