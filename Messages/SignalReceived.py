from ActorSystem.Messages import Message


class SignalReceived(Message):
    def __init__(self, sender, when_signal_received, sensor):
        super().__init__(sender)
        self.when_signal_received = when_signal_received
        self.sensor = sensor
