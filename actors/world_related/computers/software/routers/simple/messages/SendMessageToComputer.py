from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers import Computer


class SendMessageToComputer(Message):
    """
    Сообщение о том, что нужно выслать вложенное сообщение на удалённый компьютер.
    """

    def __init__(self, sender: Actor, message: Message, computer_to: Computer):
        super().__init__(sender)
        self.message = message
        self.computer_to = computer_to
