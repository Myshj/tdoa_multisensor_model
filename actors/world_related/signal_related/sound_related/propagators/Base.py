from actors.world_related import AbstractWorldRelatedActor as WorldRelatedActor
from actors.worlds import Base as World
from auxillary import Position


class Base(WorldRelatedActor):
    """
    Базовый класс для всех распространителей звуковых сигналов.
    """

    def __init__(self, position: Position, world: World, sensors: list):
        """
        Конструктор.
        :param Position position: Позиция актора в мире.
        :param World world: Мир, к которому прикреплён актор.
        :param list sensors: Сенсоры, среди которых нужно распространять сигнал.
        """
        super().__init__(position=position, world=world)
        self.sensors = sensors
