from actor_system import Actor
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators.simple import \
    SimpleEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.supervisors.tdoa_group.messages import Base


class AbstractPositionDeterminatorOperation(Base):
    """
    Базовый класс для всех сообщений об операциях с определителчми позиций.
    """

    def __init__(self, sender: Actor, position_determinator: SimpleEstimatedPositionDeterminator):
        super().__init__(sender)
        self.position_determinator = position_determinator
