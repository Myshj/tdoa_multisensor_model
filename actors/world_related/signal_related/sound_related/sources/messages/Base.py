from actor_system.messages import Message


class Base(Message):
    """
    Базовый класс для сообщений для источников сигнала .
    """

    def __init__(self, sender):
        super().__init__(sender)
