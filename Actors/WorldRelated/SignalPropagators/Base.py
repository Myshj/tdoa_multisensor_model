from Actors.WorldRelated import Base as WorldRelatedActor
from auxillary import Position
from Actors.Worlds import Base as World
from Actors.WorldRelated.Sensors import Base as Sensor


class Base(WorldRelatedActor):
    """
    Базовый класс для всех распространителей сигналов.
    """

    def __init__(self, position: Position, world: World, sensors: list):
        super().__init__(position=position, world=world)
        self.sensors = sensors
