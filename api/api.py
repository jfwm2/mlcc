from typing import Union

from fastapi import FastAPI

from mlcc.engine.engine import Engine

app = FastAPI()
engine = Engine()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/foods/{food_id}")
def read_food(food_id: str, q: Union[str, None] = None):
    return {"food_id": food_id, "q": q, "food": engine.food_data.get_food_by_name(food_id)}
