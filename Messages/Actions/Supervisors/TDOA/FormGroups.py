from .Base import Base
from ActorSystem import Actor


class FormGroups(Base):
    """
    Сообщение о том, что нужно сформировать группы из датчиков.
    """

    def __init__(self, sender: Actor, sensors: set):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param set sensors: Датчики, из которых нужно сформировать группы.
        """
        super().__init__(sender)
        self.sensors = sensors
