from enum import Enum


class BoundType(Enum):
    """
    Типы границ для интервала.
    """
    Inclusive = 1
    Exclusive = 2
