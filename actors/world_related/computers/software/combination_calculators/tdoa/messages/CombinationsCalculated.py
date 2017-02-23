from collections import Iterable

from actor_system import Actor
from .Base import Base


class CombinationsCalculated(Base):
    """
    Сообщение о том, что из списка сенсоров сформированы комбинации.
    """

    def __init__(self, sender: Actor, sensors: Iterable, combinations: set):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Iterable sensors: Сенсоры, из которых сформированы комбинации.
        :param set combinations: Сформированные комбинации.
        """
        super().__init__(sender)
        self.sensors = sensors
        self.combinations = combinations
