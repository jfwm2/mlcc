from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation


class TextClient:

    def __init__(self, client: AbstractClientImplementation) -> None:
        self.client = client
        self.repl()

    def repl(self) -> None:
        input_str = ''
        while input_str.upper() != 'X':
            current_meal_str = '' \
                if self.client.current_meal_name is None else f'[{self.client.current_meal_name}] '
            current_food_str = '' if self.client.current_food_name is None else f'[{self.client.current_food_name}] '
            input_str = input(f"[{self.client.current_date}] (L)ist, (C)hange, or s(H)ow date / "
                              f"ch(O)ose of sho(W) meal {current_meal_str}/ "
                              f"add (F)ood to meal / (A)dd, l(I)st, (D)isplay or s(E)lect food {current_food_str}/ "
                              "(S)ave / e(X)it -- Input: ")
            try:
                if input_str.upper() not in 'LCHOWFAIDESX':
                    print(f'Invalid input {input_str}')
                elif input_str.upper() == 'L':
                    self.client.display_user_data()
                elif input_str.upper() == 'C':
                    self.client.set_current_date()
                elif input_str.upper() == 'H':
                    self.client.display_meals_of_the_day()
                elif input_str.upper() == 'O':
                    self.client.set_current_meal()
                elif input_str.upper() == 'W':
                    self.client.display_current_meal()
                elif input_str.upper() == 'F':
                    self.client.add_current_food_to_current_meal()
                elif input_str.upper() == 'A':
                    self.client.add_food_data()
                elif input_str.upper() == 'I':
                    self.client.display_food_data()
                elif input_str.upper() == 'D':
                    self.client.display_food()
                elif input_str.upper() == 'E':
                    self.client.set_current_food()
                elif input_str.upper() == 'S':
                    self.client.save()
                else:
                    self.client.exit()
            except NotImplementedError as nie:
                print(f"{type(nie).__name__}: this feature was not implemented")
