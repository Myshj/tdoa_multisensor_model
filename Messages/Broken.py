from ActorSystem.Messages import Message


class Broken(Message):
    def __init__(self, sender, who):
        super().__init__(sender)
        self.who = who
