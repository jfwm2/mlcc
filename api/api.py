from datetime import date
from typing import Union

from fastapi import FastAPI

from mlcc.common.common import get_meal_type_by_name, get_meal_type_by_value
from mlcc.engine.engine import Engine
from mlcc.types.meal_type import MealType
from mlcc.types.unit_type import UnitType

app = FastAPI()
engine = Engine()


@app.get("/")
def read_root():
    return {"App": {"name": "My Little Calories Counter", "short_name": "mlcc"}}


@app.get("/engine")
def read_engine():
    return {"engine": engine.get_serializable_dict()}


@app.get("/foods")
def read_foods(show: Union[str, None] = None):
    if show is None or show != "all":
        return {"show": show, "foods": engine.food_data.get_all_food_names()}
    else:
        return {"show": "all", "foods": engine.food_data.get_serializable_dict()}


@app.get("/foods/{food_id}")
def read_food(food_id: str):
    return {"food_id": food_id, "food": engine.food_data.get_food_by_name(food_id).get_serializable_dict()}


@app.get("/types")
def read_meal_type():
    return ["meal_type", "unit_type"]


@app.get("/types/meal")
def read_meal_type():
    return {"meal_type": MealType.get_serialized_dict()}


@app.get("/types/unit")
def read_meal_type():
    return {"unit_type": UnitType.get_serialized_dict()}


@app.get("/data")
def read_foods(show: Union[str, None] = None):
    if show is None or show != "all":
        return {"show": show, "data": engine.get_user_data().get_all_dates()}
    else:
        return {"show": "all", "data": engine.get_user_data().get_serializable_dict()}


@app.get("/data/{day_date}")
def read_foods(day_date: str):
    year, month, day = map(int, day_date.split('-'))
    meals = engine.get_user_data().get_meals_of_the_day(date(year, month, day))
    return {"date": date(year, month, day), "meals": meals.get_serializable_dict()}


@app.get("/data/{day_date}/{meal_type}")
def read_foods(day_date: str, meal_type: Union[str, int]):
    actual_meal_type = None
    if meal_type.isdigit():
        actual_meal_type = get_meal_type_by_value(int(meal_type))
    else:
        actual_meal_type = get_meal_type_by_name(meal_type)
    assert actual_meal_type is not None
    year, month, day = map(int, day_date.split('-'))
    meal = engine.get_user_data().get_meals_of_the_day(date(year, month, day)).get_meal(actual_meal_type)
    return {"date": date(year, month, day), "meal": meal.get_serializable_dict()}
