from typing import Union

from fastapi import FastAPI

from mlcc.engine.engine import Engine

app = FastAPI()
engine = Engine()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/foods")
def read_food(show: Union[str, None] = None):
    if show is None or show != "all":
        return {"show": show, "foods": engine.food_data.get_all_food_names()}
    else:
        return {"show": "all", "foods": engine.food_data.get_serializable_dict()}


@app.get("/foods/{food_id}")
def read_food(food_id: str):
    return {"food_id": food_id, "food": engine.food_data.get_food_by_name(food_id).get_serializable_dict()}
