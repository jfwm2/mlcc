import json
from pathlib import Path
from typing import Dict, List, Union

from mlcc.common.defaults import DEFAULT_DATA_DIR, FOOD_DATA_FILE, USER_DATA_FILE, GLOBAL_DATA_FILE, DATA_FILES
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
        self.global_data_file = data_dir_path / GLOBAL_DATA_FILE

    def get_food_data(self) -> FoodData:
        return self.food_data

    def get_user_data(self) -> UserData:
        return self.user_data

    def save(self):
        self.food_data.save()
        self.user_data.save()
        print(f'Saving global data to {self.global_data_file}')
        with open(self.global_data_file, "w") as outfile:
            json.dump(self.get_serializable_dict(), outfile)

    def get_serializable_dict(self) -> Dict[str, Union[
        str, Dict[str, Union[str, Dict[str, Union[str, Dict[int, Dict[str, Union[int, str, Dict[str, float]]]]]]]],
        Dict[str, Union[
            str, List[Dict[str, Union[str, Dict[str, Union[float, str, Dict[str, Union[float, int, str]]]]]]]]]]]:
        return {
            'food_data': self.food_data.get_serializable_dict(),
            'user_data': self.user_data.get_serializable_dict(),
            'description': str(self),
            'type': str(self.__class__.__name__)
        }
