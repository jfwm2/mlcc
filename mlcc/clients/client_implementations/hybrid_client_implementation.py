import requests

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.common.defaults import DEFAULT_API_URL


class HybridClientImplementation(AbstractClientImplementation):

    def __init__(self, api_url=DEFAULT_API_URL) -> None:
        super().__init__()
        self.api_url = api_url

    def display_food_data(self) -> None:
        response = requests.get(f"{self.api_url}/foods")
        foods_response = response.json().get('foods', None)
        if foods_response is None:
            print("<food list could not be retrieved>")
            return None
        for name in foods_response:
            response = requests.get(f"{self.api_url}/foods/{name}")
            food_response = response.json().get('food', None)
            description = '<food description could not be retrieved>' \
                if food_response is None or 'description' not in food_response else food_response['description']
            print(f"{name}: {description}")

    @staticmethod
    def exit() -> None:
        print("Exiting Hybrid Client")
