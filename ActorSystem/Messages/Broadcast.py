from .Message import Message


class Broadcast(Message):
    def __init__(self, sender, message_to_broadcast: Message):
        super(Broadcast, self).__init__(sender)
        self.message_to_broadcast = message_to_broadcast