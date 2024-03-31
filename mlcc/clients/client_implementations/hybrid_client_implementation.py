from datetime import date
from typing import List, Optional

import requests

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_string_with_trie
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

    def get_current_food_name(self) -> str:
        if self.current_food_name is None:
            return ''
        return self.current_food_name

    def display_user_data(self) -> None:
        day_date_strings = self._get_all_date_strings()
        if day_date_strings is not None:
            for day_date in map(get_date_from_string, day_date_strings):
                self._display_meals_of_the_day(day_date)

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
