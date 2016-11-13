class Message(object):
    """
    Базовый класс для всех сообщений, принимаемых акторами.
    """

    def __init__(self, sender):
        self.sender = sender
