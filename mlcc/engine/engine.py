from pathlib import Path

from mlcc.common.defaults import DEFAULT_DATA_DIR, FOOD_DATA_FILE, USER_DATA_FILE, DATA_FILES
from mlcc.engine.food_data import FoodData
from mlcc.engine.user_data import UserData


class Engine:
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
                with open(data_file_path, "w") as outfile:
                    outfile.write("{}")

    def __init__(self, data_dir=DEFAULT_DATA_DIR) -> None:
        data_dir_path: Path = Path(data_dir).expanduser().resolve()
        Engine._create_data_files_if_not_exist(data_dir_path)
        self.food_data = FoodData(data_dir_path / FOOD_DATA_FILE)
        self.user_data = UserData(data_dir_path / USER_DATA_FILE, self.food_data)

    def get_food_data(self) -> FoodData:
        return self.food_data

    def get_user_data(self) -> UserData:
        return self.user_data

    def save(self):
        self.food_data.save()
        self.user_data.save()
