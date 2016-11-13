from ActorSystem.Messages import Message


class PropagateSignal(Message):
    def __init__(self, sender,
                 source_position):
        super().__init__(sender)
        self.source_position = source_position
