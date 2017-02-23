from actor_system.broadcasters import Broadcaster
from actor_system.broadcasters.messages import Broadcast
from actor_system.messages import Message
from actors.world_related import AbstractWorldRelatedActor
from actors.worlds import Base as World
from auxillary import Position
from .messages.actions.hardware_actions import *
from .messages.events.hardware_events import *


class Computer(AbstractWorldRelatedActor):
    def __init__(
            self,
            position: Position,
            world: World,
    ):
        super().__init__(position, world)
        self.connected_hardware = set()
        self.hardware_events_broadcaster = Broadcaster()

    def on_message(self, message: Message):
        if isinstance(message, AbstractHardwareAction):
            self.on_hardware_action(message)

    def on_hardware_action(self, message: AbstractHardwareAction):
        if isinstance(message, ConnectHardware):
            self.on_connect_hardware(message.hardware)
        elif isinstance(message, DisconnectHardware):
            self.on_disconnect_hardware(message.hardware)

    def on_connect_hardware(self, hardware):
        self._connect_hardware(hardware)
        self._notify_that_hardware_connected(hardware)

    def on_disconnect_hardware(self, hardware):
        self._disconnect_hardware(hardware)
        self._notify_that_hardware_disconnected(hardware)

    def _connect_hardware(self, hardware):
        self.connected_hardware.add(hardware)

    def _disconnect_hardware(self, hardware):
        self.connected_hardware.remove(hardware)

    def _notify_that_hardware_connected(self, hardware):
        self.hardware_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=HardwareConnected(
                    sender=self,
                    hardware=hardware
                )
            )
        )

    def _notify_that_hardware_disconnected(self, hardware):
        self.hardware_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=HardwareDisconnected(
                    sender=self,
                    hardware=hardware
                )
            )
        )
