from ActorSystem import Actor


class Message(object):
    """
    Базовый класс для всех сообщений, принимаемых акторами.
    """

    def __init__(self, sender: Actor):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        """
        self.sender = sender
