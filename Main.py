import argparse

from mlcc.my_little_calorie_counter import MyLittleCalorieCounter
from mlcc.types.client_implementation_type import ClientImplementationType

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_implementation_type",
                        choices=[cit.name.lower() for cit in ClientImplementationType],
                        help="Client implementation type")

    args = parser.parse_args()
    client_implementation_type = ''
    for cit in ClientImplementationType:
        if cit.name.lower() == args.client_implementation_type:
            client_implementation_type = cit
            break

    MyLittleCalorieCounter(client_implementation_type)
