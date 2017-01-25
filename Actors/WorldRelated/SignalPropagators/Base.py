from Actors.WorldRelated import Base as WorldRelatedActor
from auxillary import Position
from Actors.Worlds import Base as World


class Base(WorldRelatedActor):
    """
    Базовый класс для всех распространителей сигналов.
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
