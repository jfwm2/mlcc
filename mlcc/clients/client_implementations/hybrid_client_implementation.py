from typing import List, Optional

import requests

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_string_with_trie
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

    def set_current_food(self) -> None:
        food_names = self._get_food_names()
        if food_names is not None:
            self.current_food_name = input_string_with_trie("Name of the food to select", Trie(food_names))

    @staticmethod
    def exit() -> None:
        print("Exiting Hybrid Client")

    def _get_food_names(self) -> Optional[List[str]]:
        response = requests.get(f"{self.api_url}/foods")
        foods_response = response.json().get('foods', None)
        if foods_response is None:
            print("<food list could not be retrieved>")
        return foods_response
