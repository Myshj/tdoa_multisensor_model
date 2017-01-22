from ActorSystem import Actor
from Actors.Worlds import Base as World


class Base(Actor):
    """
    Базовый класс для всех источников сигнала.
    """

    def __init__(self, world: World):
        """
        Конструктор.
        :param World world: Мир, в котором существует источник сигнала.
        """
        super().__init__()
        self.world = world
