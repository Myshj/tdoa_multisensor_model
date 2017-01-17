from .Base import Base
from ActorSystem import Actor
from collections import Iterable


class Locate(Base):
    """
    Сообщение о том, что нужно вычислить положение объекта на основании задержек прихода сигнала от него.
    """

    def __init__(self, sender: Actor, transit_times: Iterable):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Iterable transit_times: Задержки прихода сигнала от объекта.
        """
        super().__init__(sender)
        self.transit_times = transit_times
