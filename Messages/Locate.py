from ActorSystem.Messages import Message

class Locate(Message):
    def __init__(self, sender, transit_times):
        super().__init__(sender)
        self.transit_times = transit_times
