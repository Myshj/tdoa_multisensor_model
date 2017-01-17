from ActorSystem.Messages import Message
from ActorSystem import Actor
from collections import Iterable


class Base(Message):
    """
    Базовый класс для сообщений о сигналах.
    """

    def __init__(self, sender: Actor, signal):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param signal: Сигнал, о котором идёт речь.
        """
        super().__init__(sender)
        self.signal = signal
