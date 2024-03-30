from mlcc.clients.client_implementations.abstract_client_implementation import AbstractClientImplementation
from mlcc.common.defaults import DEFAULT_API_URL


class HybridClientImplementation(AbstractClientImplementation):

    def __init__(self, api_url=DEFAULT_API_URL) -> None:
        super().__init__()
        self.api_url = api_url

    @staticmethod
    def exit() -> None:
        print("Exiting Hybrid Client")
