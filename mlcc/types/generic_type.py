from enum import Enum


class GenericType(Enum):

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> int:
        return self.value
