from .Message import Message


class AddListener(Message):
    def __init__(self, sender, listener):
        super(AddListener, self).__init__(sender)
        self.listener = listener
