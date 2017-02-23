from actor_system import Actor
from actor_system.messages import Message


class ReceiveMessage(Message):
    """
    Сообщение о том, что сетевой адаптер должен получить вложенное сообщение.
    """

    def __init__(self, sender: Actor, message: Message):
        super().__init__(sender)
        self.message = message
