from .Base import Base
from ActorSystem import Actor
from collections import Iterable


class FormGroups(Base):
    """
    Сообщение о том, что из списка сенсоров нужно сформировать группы.
    """

    def __init__(self, sender: Actor, sensors: Iterable):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Iterable sensors: Сенсоры, из которых нужно сформировать группы.
        """
        super().__init__(sender)
        self.sensors = sensors
