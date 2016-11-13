from ActorSystem.Messages import Message


class SignalSourceSendSignal(Message):
    def __init__(self, sender):
        super().__init__(sender)
