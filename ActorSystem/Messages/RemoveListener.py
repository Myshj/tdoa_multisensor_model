from .Message import Message


class RemoveListener(Message):
    def __init__(self, sender, listener):
        super(RemoveListener, self).__init__(sender)
        self.listener = listener
