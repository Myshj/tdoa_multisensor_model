from ActorSystem import Actor
from Actors.Worlds import Base as World


class Base(Actor):
    """
    Базовый класс для всех сенсоров.
    """

    def __init__(self, world: World):
        """
        Конструктор.
        :param World world: Мир, в котором существует датчик.
        """
        super().__init__()
        self.world = world
