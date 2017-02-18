from actor_system import Actor
from actor_system.messages.Message import Message


class Broadcast(Message):
    """
    Этим сообщением говорим, что нужно размножить вложенное сообщение.
    """

    def __init__(self, sender: Actor, message: Message):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Message message: Сообщение для размножения.
        """
        super().__init__(sender)
        self.message = message
