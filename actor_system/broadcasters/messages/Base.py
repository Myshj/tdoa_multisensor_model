from actor_system import Actor
from actor_system.messages import Message


class Base(Message):
    """
    Базовый класс для сообщений об акторах.
    """

    def __init__(self, sender: Actor, actor: Actor):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Actor actor: Актор о котором идёт речь.
        """
        super().__init__(sender)
        self.actor = actor
