from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.clients.text_input import input_date, input_meal_type, input_float, input_string, input_unit_type, \
    input_string_with_trie
from mlcc.common.common import is_quantity_valid, guess_quantity
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
                quantity = input_float(f"Quantity of {name}: ")
                unit_type = input_unit_type()
                unit_symbol = input_string("Unit symbol")
                valid_quantity = is_quantity_valid(quantity, unit_type, unit_symbol)
                if not valid_quantity:
                    print(f"the quantity entered for food {name}; {quantity} {unit_symbol} "
                          f"({unit_type.name.lower()}) is not valid")

            guessed_quantity = guess_quantity(quantity, unit_type, unit_symbol)
            calories = input_float(f"Calories in {guessed_quantity} of {name}: ")
            self.engine.get_food_data().add(
                name=name, calories=calories, quantity=quantity, unit_type=unit_type, unit_symbol=unit_symbol)
            print(f"{self.engine.get_food_data().get_food_by_name(name)} entered")

    def set_current_date(self) -> None:
        self.current_date = input_date()

    def display_food_data(self) -> None:
        for name in self.engine.get_food_data().get_all_food_names():
            print(f"{name}: {self.engine.get_food_data().get_food_by_name(name)}")

    def display_food(self) -> None:
        if self.current_food is None:
            print('No food selected')
        else:
            print(self.current_food)

    def set_current_food(self) -> None:
        food_name = input_string_with_trie("Name of the food to select", self.food_trie)
        self.current_food = self.engine.get_food_data().get_food_by_name(food_name)

    def get_current_food_name(self) -> str:
        if self.current_food is None:
            return ''
        return self.current_food.get_name()

    def display_user_data(self) -> None:
        for day_date in self.engine.get_user_data().get_all_dates():
            print(f"{day_date} -- {self.engine.get_user_data().get_meals_of_the_day(day_date).calories():2f} calories")
            for meal in self.engine.get_user_data().get_meals_of_the_day(day_date).get_meals().values():
                print(f"{meal.get_type().get_name().capitalize()}:",
                      ', '.join([f"{quantity} {food.get_nutrition_data().get_quantity().get_unit_symbol()} of "
                                 f"{food.get_name()}" for food, quantity in meal.menu.items()]),
                      f'total of {meal.get_calories_in_meal():2f} calories')

    def display_meals_of_the_day(self) -> None:
        self.engine.get_user_data().get_or_create_meals_of_the_day(self.current_date).display()

    def set_current_meal(self) -> None:
        self.current_meal = (self.engine.get_user_data().get_or_create_meals_of_the_day(self.current_date).select_meal(
            input_meal_type()))

    def get_current_meal_name(self) -> str:
        if self.current_meal is None:
            return ''
        return self.current_meal.get_type().name

    def display_current_meal(self) -> None:
        if self.current_meal is None:
            print('No meal selected')
        else:
            self.current_meal.display()

    def add_current_food_to_current_meal(self):
        if self.current_meal is None:
            print('No meal selected')
        if self.current_food is None:
            print('No food selected')
        if self.current_meal is not None and self.current_food is not None:
            quantity = (input_float(f"How much {self.current_food.unit_symbol} of "
                                    f"{self.current_food.name} would you like to add: "))
            self.current_meal.add_food(self.current_food, quantity)
            new_quantity = self.current_meal.get_quantity_of_food_for_cuurent_meal()
            print(f"{quantity} {food.get_nutrition_data().get_quantity().get_unit_symbol()} {food.get_name()} "
                  f"added to {self.type.get_name().lower()}; "
                  f"total {new_quantity} {food.get_nutrition_data().get_quantity().get_unit_type()} -> "
                  f"{quantity * food.get_nutrition_data().get_calories_per_unit():2f} cal")

    def save(self) -> None:
        self.engine.get_food_data().save()
        self.engine.get_user_data().save()

    @staticmethod
    def exit() -> None:
        print("Exiting")
