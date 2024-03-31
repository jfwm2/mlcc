from datetime import date
from typing import Dict, List, Optional

import requests

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_string_with_trie, input_ad_hoc_type
from mlcc.common.common import get_date_from_string
from mlcc.common.defaults import DEFAULT_API_URL
from mlcc.common.trie import Trie


class HybridClientImplementation(AbstractClientImplementation):

    def __init__(self, api_url=DEFAULT_API_URL) -> None:
        super().__init__()
        self.api_url = api_url

    def display_food_data(self) -> None:
        food_names = self._get_food_names()
        if food_names is not None:
            for name in food_names:
                response = requests.get(f"{self.api_url}/foods/{name}")
                food_response = response.json().get('food', None)
                description = '<food description could not be retrieved>' \
                    if food_response is None or 'description' not in food_response else food_response['description']
                print(f"{name}: {description}")

    def display_food(self) -> None:
        if self.current_food_name is None:
            print('No food selected')
        else:
            response = requests.get(f"{self.api_url}/foods/{self.current_food_name}")
            food_response = response.json().get('food', None)
            description = '<food description could not be retrieved>' \
                if food_response is None or 'description' not in food_response else food_response['description']
            print(description)

    def set_current_food(self) -> None:
        food_names = self._get_food_names()
        if food_names is not None:
            self.current_food_name = input_string_with_trie("Name of the food to select", Trie(food_names))

    def display_user_data(self) -> None:
        day_date_strings = self._get_all_date_strings()
        if day_date_strings is not None:
            for day_date in map(get_date_from_string, day_date_strings):
                self._display_meals_of_the_day(day_date)

    def display_meals_of_the_day(self) -> None:
        self._display_meals_of_the_day(self.current_date)

    def set_current_meal(self) -> None:
        meal_type_dict = self._get_meal_type_dict()
        if meal_type_dict is not None:
            meal_type_value = input_ad_hoc_type(meal_type_dict, 'Meal')
            self.current_meal_name = meal_type_dict[meal_type_value].capitalize()

    def display_current_meal(self) -> None:
        if self.current_meal_name is None:
            print('No meal selected')
        else:
            response = requests.get(f"{self.api_url}/data/{self.current_date}/{self.current_meal_name}")
            meal_response = response.json().get('meal', None)
            if meal_response is None or 'description' not in meal_response:
                print(f"<meal description could not be retrieved for {self.current_meal_name} of {self.current_date}>")
            else:
                print(meal_response['description'])

    @staticmethod
    def exit() -> None:
        print("Exiting Hybrid Client")

    def _get_food_names(self) -> Optional[List[str]]:
        response = requests.get(f"{self.api_url}/foods")
        foods_response = response.json().get('foods', None)
        if foods_response is None:
            print("<food list could not be retrieved>")
        return foods_response

    def _get_all_date_strings(self) -> Optional[List[str]]:
        response = requests.get(f"{self.api_url}/data")
        data_response = response.json().get('data', None)
        if data_response is None:
            print("<data list could not be retrieved>")
        return data_response

    def _display_meals_of_the_day(self, day_date: date) -> None:
        response = requests.get(f"{self.api_url}/data/{day_date}")
        meals_response = response.json().get(str(day_date), None)
        if (meals_response is None or 'description' not in meals_response or
                'meals' not in meals_response or not isinstance(meals_response['meals'], dict)):
            print(f"<meals data could not be retrieved for {day_date}>")
        else:
            print(meals_response['description'])
            for meal_type, meal in meals_response['meals'].items():
                if 'description' in meal:
                    print(meal['description'])
                else:
                    print(f"<meal description could not be retrieved for meal type {meal_type}>")

    def _get_meal_type_dict(self) -> Optional[Dict[int, str]]:
        response = requests.get(f"{self.api_url}/types/meal")
        meal_type_response = response.json().get('meal_type', None)
        if meal_type_response is None or not isinstance(meal_type_response, dict):
            print("<meal type definition could not be retrieved>")
            return None
        return {int(k): v for k, v in meal_type_response.items()}
