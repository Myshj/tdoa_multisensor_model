from ActorSystem.Messages import Message


class FormGroups(Message):
    def __init__(self, sender, sensors):
        super().__init__(sender)
        self.sensors = sensors
