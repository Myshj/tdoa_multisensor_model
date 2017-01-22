from ActorSystem import Actor


class Base(Actor):
    """
    Базовый класс для миров.
    """

    def __init__(self, name: str):
        """
        Конструктор.
        :param str name: Название мира.
        """
        super().__init__()
        self.name = name
