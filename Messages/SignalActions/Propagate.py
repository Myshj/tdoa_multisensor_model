from .Base import Base
from ActorSystem import Actor
from collections import Iterable


class Propagate(Base):
    """
    Сообщение о том, что нужно распространить сигнал, начиная с некоторой позиции.
    """

    def __init__(self, sender: Actor, signal, source_position: Iterable):
        """

        :param Actor sender: Адресант сообщения.
        :param signal:
        :param Iterable source_position: Позиция источника сигнала.
        """
        super().__init__(sender, signal)
        self.source_position = source_position
