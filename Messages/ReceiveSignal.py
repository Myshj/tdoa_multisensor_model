from ActorSystem.Messages import Message


class ReceiveSignal(Message):
    def __init__(self, sender, when_signal_received):
        super().__init__(sender)
        self.when_signal_received = when_signal_received
