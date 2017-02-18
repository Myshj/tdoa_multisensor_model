from datetime import datetime

from actor_system import Actor
from actor_system.messages import Message


class ReceiveSignal(Message):
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
        super().__init__(sender)
        self.signal = signal
        self.when = when
