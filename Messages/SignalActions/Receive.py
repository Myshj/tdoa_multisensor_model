from .Base import Base
from ActorSystem import Actor
from datetime import datetime


class Receive(Base):
    """
    Сообщение о том, что в некоторый момент времени нужно получить сигнал.
    """

    def __init__(self, sender: Actor, signal, when: datetime):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param signal: Сигнал для получения.
        :param datetime when: Когда получить сигнал.
        """
        super().__init__(sender, signal)
        self.when = when
