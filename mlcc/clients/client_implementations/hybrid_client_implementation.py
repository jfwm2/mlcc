from datetime import date
from typing import Dict, List, Optional, Any

import requests

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_ad_hoc_type, input_float, input_string, input_string_with_trie
from mlcc.common.common import get_date_from_string
from mlcc.common.defaults import DEFAULT_API_URL, ROUNDING_DECIMALS_IN_FLOAT
from mlcc.common.trie import Trie


class HybridClientImplementation(AbstractClientImplementation):

    def __init__(self, api_url=DEFAULT_API_URL) -> None:
        super().__init__()
        self.api_url = api_url

    def add_food_data(self) -> None:
        food_names = self._get_food_names()
        if food_names is None:
            return None
        name = input_string("New food name")
        if name in food_names:
            print('food name is already present, please choose another one')
            return None
        unit_type_dict = self._get_unit_type_dict()
        if unit_type_dict is None:
            return None

        quantity, unit_type_value, unit_symbol, guessed_quantity = 0, 0, '', None
        while guessed_quantity is None:
            unit_type_value = input_ad_hoc_type(unit_type_dict, 'Unit')
            unit_symbol = input_string("Unit symbol")
            quantity = input_float(f"Quantity of {name}")
            response_guessed = requests.post(f"{self.api_url}/types/unit/guessed_quantity", json={
                'value': quantity,
                'unit_type': unit_type_value,
                'unit_symbol': unit_symbol
            })
            guessed_quantity = response_guessed.json().get("guessed_quantity", None)
            if guessed_quantity is None:
                print(f"the quantity entered for food {name}; "
                      f"{quantity} {unit_symbol} ({unit_type_value}) is not valid")

        calories = input_float(f"Calories in {guessed_quantity} of {name}")
        response_add = requests.post(f"{self.api_url}/foods/{name}", json={
            'name': name,
            'nutrition_data': {'calories': calories,
                               'quantity': {
                                   'value': quantity, 'unit_type': unit_type_value, 'unit_symbol': unit_symbol}}})
        food_response = response_add.json().get('food', None)
        if food_response is None or 'description' not in food_response:
            print(f"An issue occurred when adding food {name}")
        else:
            print(f"{food_response['description']} entered")

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

    def add_current_food_to_current_meal(self) -> None:
        if self.current_meal_name is None:
            print('No meal selected')
        if self.current_food_name is None:
            print('No food selected')
        if self.current_meal_name is not None and self.current_food_name is not None:
            food = self._get_food_dict(self.current_food_name)
            if (food is None or 'nutrition_data' not in food
                    or not self._is_valid_nutrition_data(food['nutrition_data'])):
                print(f'Food {self.current_food_name} cannot be selected or contains invalid nutrition data')
            quantity = (input_float(f"How much {food['nutrition_data']['quantity']['unit_symbol']} of "
                                    f"{self.current_food_name} to add to {self.current_meal_name}"))
            response = requests.post(
                f"{self.api_url}/data/{self.current_date}/{self.current_meal_name}/add/{self.current_food_name}",
                params={'q': quantity})
            meal_response = response.json().get('meal', None)
            if (meal_response is None or 'menu' not in meal_response
                    or self.current_food_name not in meal_response['menu']
                    or meal_response['menu'][self.current_food_name] is None):
                print(f"<updated quantity of {self.current_food_name} "
                      f"could not be retrieved for {self.current_meal_name} of {self.current_date}>")
            else:
                new_quantity = None
                try:
                    new_quantity = float(meal_response['menu'][self.current_food_name])
                except ValueError:
                    print(f"<invalid quantity ({meal_response['menu'][self.current_food_name]}) of "
                          f"{self.current_food_name} retrieved for {self.current_meal_name} of {self.current_date}>")
                if new_quantity is not None:
                    new_calories = new_quantity * float(food['nutrition_data']['calories_per_unit'])
                    print(f"{quantity} {food['nutrition_data']['quantity']['unit_symbol']} of {self.current_food_name} "
                          f"added to {self.current_meal_name.lower()}; total {new_quantity} "
                          f"{food['nutrition_data']['quantity']['unit_symbol']} -> "
                          f"{round(new_calories, ROUNDING_DECIMALS_IN_FLOAT)} cal")

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

    def _get_unit_type_dict(self) -> Optional[Dict[int, str]]:
        response = requests.get(f"{self.api_url}/types/unit")
        unit_type_response = response.json().get('unit_type', None)
        if unit_type_response is None or not isinstance(unit_type_response, dict):
            print("<unit type definition could not be retrieved>")
            return None
        return {int(k): v for k, v in unit_type_response.items()}

    def _get_food_dict(self, name: str) -> Optional[Dict[str, Any]]:
        response = requests.get(f"{self.api_url}/foods/{name}")
        food_response = response.json().get('food', None)
        return food_response

    def _is_valid_nutrition_data(self, nutrition_data: Dict[str, Any]) -> bool:
        if (not isinstance(nutrition_data, dict)
                or 'calories' not in nutrition_data or nutrition_data['calories'] is None
                or 'calories_per_unit' not in nutrition_data or nutrition_data['calories_per_unit'] is None
                or 'quantity' not in nutrition_data or not self._is_valid_quantity(nutrition_data['quantity'])):
            return False
        try:
            float(nutrition_data['calories'])
            float(nutrition_data['calories_per_unit'])
        except ValueError:
            return False
        return True

    @staticmethod
    def _is_valid_quantity(quantity: Dict[str, Any]) -> bool:
        if (not isinstance(quantity, dict) or 'value' not in quantity or quantity['value'] is None
                or 'unit_type' not in quantity or quantity['unit_type'] is None
                or 'unit_symbol' not in quantity or quantity['unit_symbol'] is None):
            return False
        try:
            float(quantity['value'])
            int(quantity['unit_type'])
        except ValueError:
            return False
        return True
