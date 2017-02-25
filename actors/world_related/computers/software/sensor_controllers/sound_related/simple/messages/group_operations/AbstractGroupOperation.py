from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers.software.sensor_groups.TDOASensorGroup import TDOASensorGroup


class AbstractGroupOperation(Message):
    """
    Базовый класс для всех сообщений о действиях с группами датчиков.
    """

    def __init__(self, sender: Actor, sensor_group: TDOASensorGroup):
        super().__init__(sender)
        self.sensor_group = sensor_group
