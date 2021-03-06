from collections import Iterable

from actor_system import Actor
from .Base import Base


class CalculateCombinations(Base):
    """
    Сообщение о том, что из списка сенсоров нужно сформировать комбинации.
    """

    def __init__(self, sender: Actor, sensor_controllers: Iterable):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Iterable sensor_controllers: Сенсоры, из которых нужно сформировать комбинации.
        """
        super().__init__(sender)
        self.sensor_controllers = sensor_controllers
