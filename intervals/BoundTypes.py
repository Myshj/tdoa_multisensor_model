from enum import Enum


class BoundType(Enum):
    """
    Типы границ для интервала.
    """
    Inclusive = 1
    Exclusive = 2

    @staticmethod
    def from_string(string: str):
        return {
            string == 'inclusive': BoundType.Inclusive,
            string == 'exclusive': BoundType.Exclusive,
        }[True]
