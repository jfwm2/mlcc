from datetime import date

from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_meal_type, input_float, input_string, input_unit_type, input_string_with_trie
from mlcc.common.common import is_quantity_valid, guess_quantity, get_meal_type_by_name
from mlcc.common.trie import Trie
from mlcc.engine.engine import Engine
from mlcc.types.unit_type import UnitType


class EngineClientImplementation(AbstractClientImplementation):

    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine
        self.food_trie = Trie(engine.get_food_data().get_all_food_names())

    def add_food_data(self) -> None:
        name = input_string("New food name")
        if self.engine.get_food_data().exists(name):
            print('food name is already present, please choose another one')
        else:
            quantity = 0
            unit_type = UnitType.NONE
            unit_symbol = ''
            valid_quantity = False
            while not valid_quantity:
                unit_type = input_unit_type()
                unit_symbol = input_string("Unit symbol")
                quantity = input_float(f"Quantity of {name}: ")
                valid_quantity = is_quantity_valid(quantity, unit_type, unit_symbol)
                if not valid_quantity:
                    print(f"the quantity entered for food {name}; {quantity} {unit_symbol} "
                          f"({unit_type.name.lower()}) is not valid")

            guessed_quantity = guess_quantity(quantity, unit_type, unit_symbol)
            calories = input_float(f"Calories in {guessed_quantity} of {name}: ")
            self.engine.get_food_data().add(
                name=name, calories=calories, quantity=quantity, unit_type=unit_type, unit_symbol=unit_symbol)
            print(f"{self.engine.get_food_data().get_food_by_name(name)} entered")

    def display_food_data(self) -> None:
        for name in self.engine.get_food_data().get_all_food_names():
            print(f"{name}: {self.engine.get_food_data().get_food_by_name(name)}")

    def display_food(self) -> None:
        if self.current_food_name is None:
            print('No food selected')
        else:
            print(self.engine.get_food_data().get_food_by_name(self.current_food_name))

    def set_current_food(self) -> None:
        self.current_food_name = input_string_with_trie("Name of the food to select", self.food_trie)

    def display_user_data(self) -> None:
        for day_date in self.engine.get_user_data().get_all_dates():
            self._display_meals_of_the_day(day_date)

    def display_meals_of_the_day(self) -> None:
        self._display_meals_of_the_day(self.current_date)

    def set_current_meal(self) -> None:
        self.current_meal_name = (self.engine.get_user_data().get_or_create_meals_of_the_day(self.current_date).
                                  select_meal(input_meal_type()).get_type().get_name()).capitalize()

    def display_current_meal(self) -> None:
        if self.current_meal_name is None:
            print('No meal selected')
        else:
            meal_type = get_meal_type_by_name(self.current_meal_name)
            print(self.engine.get_user_data().get_or_create_meals_of_the_day(self.current_date).get_meal(meal_type))

    def add_current_food_to_current_meal(self):
        if self.current_meal_name is None:
            print('No meal selected')
        if self.current_food_name is None:
            print('No food selected')
        if self.current_meal_name is not None and self.current_food_name is not None:
            food = self.engine.get_food_data().get_food_by_name(self.current_food_name)
            if food is None:
                print('No food selected')
            meal_type = get_meal_type_by_name(self.current_meal_name)
            meal = self.engine.get_user_data().get_or_create_meals_of_the_day(self.current_date).get_meal(meal_type)
            quantity = (input_float(f"How much {food.get_nutrition_data().get_quantity().get_unit_symbol()} of "
                                    f"{food.get_name()} to add to {meal.get_type().get_name().capitalize()}"))
            meal.add_food(food, quantity)
            new_quantity = meal.get_quantity_in_meal(food)
            print(f"{quantity} {food.get_nutrition_data().get_quantity().get_unit_symbol()} {food.get_name()} "
                  f"added to {meal.get_type().get_name().lower()}; "
                  f"total {new_quantity} {food.get_nutrition_data().get_quantity().get_unit_type()} -> "
                  f"{new_quantity * food.get_nutrition_data().get_calories_per_unit():2f} cal")

    def save(self) -> None:
        self.engine.save()

    @staticmethod
    def exit() -> None:
        print("Exiting")

    def _display_meals_of_the_day(self, day_date: date) -> None:
        meals = self.engine.get_user_data().get_meals_of_the_day(day_date)
        print(meals)
        for meal in meals.get_meals().values():
            print(meal)
