from .BoundType import BoundType


class IntervalBound(object):
    """
    Граница интервала.
    """

    def __init__(self, value, bound_type: BoundType):
        """
        Конструктор.
        :param value: Значение границы.
        :param BoundType bound_type: Тип границы.
        """
        self.value = value
        self.bound_type = bound_type
