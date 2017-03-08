from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators.simple import \
    SimpleEstimatedPositionDeterminator


class AbstractPositionDeterminatorOperation(Message):
    """
    Базовый класс для всех сообщений об операциях с определителчми позиций.
    """

    def __init__(
            self,
            sender: Actor,
            position_determinator: SimpleEstimatedPositionDeterminator
    ):
        super().__init__(sender)
        self.position_determinator = position_determinator
