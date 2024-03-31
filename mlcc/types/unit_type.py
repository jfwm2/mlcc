from typing import Dict

from mlcc.types.generic_type import GenericType


class UnitType(GenericType):
    NONE = 0
    MASS = 1
    VOLUME = 2

    @staticmethod
    def get_serialized_dict() -> Dict[int, str]:
        return {t.value: t.name for t in UnitType}
