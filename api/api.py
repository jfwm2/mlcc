from typing import Union

from fastapi import FastAPI, HTTPException

from mlcc.common.common import get_date_from_string, get_meal_type_by_name, get_meal_type_by_value
from mlcc.engine.engine import Engine
from mlcc.types.meal_type import MealType
from mlcc.types.unit_type import UnitType

app = FastAPI()
engine = Engine()


@app.get("/")
def read_app():
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
    food = engine.food_data.get_food_by_name(food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return {"food_id": food_id, "food": food.get_serializable_dict()}


@app.get("/types")
def read_types():
    return ["meal_type", "unit_type"]


@app.get("/types/meal")
def read_meal_type():
    return {"meal_type": MealType.get_serialized_dict()}


@app.get("/types/unit")
def read_unit_type():
    return {"unit_type": UnitType.get_serialized_dict()}


@app.get("/data")
def read_data(show: Union[str, None] = None):
    if show is None or show != "all":
        return {"show": show, "data": engine.get_user_data().get_all_dates()}
    else:
        return {"show": "all", "data": engine.get_user_data().get_serializable_dict()}


@app.get("/data/{day_date}")
def read_data_date(day_date: str):
    actual_date = get_date_from_string(day_date)
    if actual_date is None:
        raise HTTPException(status_code=400, detail="Invalid date (YYYY-MM-DD expected)")

    meals = engine.get_user_data().get_or_create_meals_of_the_day(actual_date)
    if meals is None:
        raise HTTPException(status_code=404, detail="No meals found for this date")

    return {actual_date: meals.get_serializable_dict()}


@app.get("/data/{day_date}/{meal_type}")
def read_data_date_meal(day_date: str, meal_type: Union[str, int]):
    actual_date = get_date_from_string(day_date)
    if actual_date is None:
        raise HTTPException(status_code=400, detail="Invalid date (YYYY-MM-DD expected)")

    meals = engine.get_user_data().get_meals_of_the_day(actual_date)
    if meals is None:
        raise HTTPException(status_code=404, detail="No meals found for this date")

    if meal_type.isdigit():
        actual_meal_type = get_meal_type_by_value(int(meal_type))
    else:
        actual_meal_type = get_meal_type_by_name(meal_type)
    if actual_meal_type is None:
        raise HTTPException(status_code=404, detail="Meal type not found for this date")

    meal = meals.get_meal(actual_meal_type)
    return {"date": actual_date, "meal": meal.get_serializable_dict()}
