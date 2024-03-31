from typing import Dict

from mlcc.types.generic_type import GenericType


class MealType(GenericType):
    OTHER = 0
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4

    @staticmethod
    def get_serialized_dict() -> Dict[int, str]:
        return {t.value: t.name for t in MealType}
