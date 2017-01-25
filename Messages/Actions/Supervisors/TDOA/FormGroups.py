from .Base import Base
from ActorSystem import Actor


class FormGroups(Base):
    """
    Сообщение о том, что нужно сформировать группы из датчиков.
    """

    def __init__(self, sender: Actor, sensors: list, combinations: set):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        """
        super().__init__(sender)
        self.sensors = sensors
        self.combinations = combinations
