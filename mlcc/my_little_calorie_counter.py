from mlcc.clients.client_implementations.engine_client_implementation import EngineClientImplementation
from mlcc.clients.text_client import TextClient
from mlcc.defaults import DEFAULT_DATA_DIR
from mlcc.engine.engine import Engine


class MyLittleCalorieCounter:

    def __init__(self, data_dir=DEFAULT_DATA_DIR) -> None:
        engine = Engine(data_dir=data_dir)
        client = EngineClientImplementation(engine)
        TextClient(client)
