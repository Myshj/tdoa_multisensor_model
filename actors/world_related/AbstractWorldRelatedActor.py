from actor_system import Actor
from actors.worlds import Base as World
from auxillary import Position


class AbstractWorldRelatedActor(Actor):
    """
    Базовый класс для всех акторов, существующих в мирах.
    """

    def __init__(self, position: Position, world: World):
        """
        Конструктор.
        :param Position position: Позиция в мире.
        :param World world: Мир, в котором существует актор.
        """
        super().__init__()
        self.position = position
        self.world = world
