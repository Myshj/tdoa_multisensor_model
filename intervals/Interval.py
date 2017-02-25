from .IntervalBound import IntervalBound
from .BoundType import BoundType


class Interval(object):
    """
    Численный интервал.
    """

    def __init__(self, left_bound: IntervalBound, right_bound: IntervalBound):
        """
        Конструктор.
        :param IntervalBound left_bound: Левая граница.
        :param IntervalBound right_bound: Правая граница.
        """
        self.left_bound = left_bound
        self.right_bound = right_bound

    def contains_value(self, value):
        return self.value_is_in_left_bound(value) and self.value_is_in_right_bound(value)

    def value_is_in_left_bound(self, value):
        if self.left_bound.bound_type == BoundType.Inclusive:
            if value < self.left_bound.value:
                return False
        elif self.left_bound.bound_type == BoundType.Exclusive:
            if value <= self.left_bound.value:
                return False
        return True

    def value_is_in_right_bound(self, value):
        if self.right_bound.bound_type == BoundType.Inclusive:
            if value > self.right_bound.value:
                return False
        elif self.right_bound.bound_type == BoundType.Exclusive:
            if value >= self.right_bound.value:
                return False
        return True
