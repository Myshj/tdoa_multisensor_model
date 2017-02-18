from .Base import Base
from auxillary import Position
from actors.worlds import Base as World
from actor_system import Broadcaster


class Simple(Base):
    def __init__(self, position: Position, world: World):
        super().__init__(position, world)
        self.message_received_broadcaster = Broadcaster()
        self.want_to_transmit_message_broadcaster = Broadcaster()
