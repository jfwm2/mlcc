from mlcc.clients.client_implementations.engine_client_implementation import EngineClientImplementation
from mlcc.clients.client_implementations.hybrid_client_implementation import HybridClientImplementation
from mlcc.clients.text_client import TextClient
from mlcc.common.defaults import DEFAULT_CLIENT_IMPLEMENTATION_TYPE, DEFAULT_DATA_DIR, DEFAULT_API_URL
from mlcc.engine.engine import Engine
from mlcc.types.client_implementation_type import ClientImplementationType


class MyLittleCalorieCounter:

    def __init__(self, client_type: ClientImplementationType = DEFAULT_CLIENT_IMPLEMENTATION_TYPE,
                 data_dir: str = DEFAULT_DATA_DIR, api_url: str = DEFAULT_API_URL) -> None:
        if client_type == ClientImplementationType.ENGINE:
            client = EngineClientImplementation(Engine(data_dir=data_dir))
        elif client_type == ClientImplementationType.HYBRID:
            client = HybridClientImplementation(api_url=api_url)
        else:
            raise NotImplementedError

        TextClient(client)
