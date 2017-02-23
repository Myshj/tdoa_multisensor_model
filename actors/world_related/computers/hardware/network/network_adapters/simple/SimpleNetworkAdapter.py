from actor_system import Broadcaster
from actor_system.messages import Message
from actor_system.broadcasters.messages import Broadcast
from actors.worlds import Base as World
from auxillary import Position
from actors.world_related.computers.hardware.network.network_adapters.AbstractNetworkAdapter import \
    AbstractNetworkAdapter
from actors.world_related.computers.hardware.network.network_adapters.simple.messages import *


class SimpleNetworkAdapter(AbstractNetworkAdapter):
    """
    Простейший сетевой адаптер.
    """

    def __init__(self, position: Position, world: World):
        super().__init__(position, world)
        self.message_received_broadcaster = Broadcaster()
        self.want_to_transmit_message_broadcaster = Broadcaster()

    def on_message(self, message: Message):
        if isinstance(message, ReceiveMessage):
            self.on_receive_message(message.message)
        elif isinstance(message, TransmitMessage):
            self.on_transmit_message(message.message, message.adapter_to)

    def on_receive_message(self, message: Message):
        self._receive_message(message)

    def on_transmit_message(self, message: Message, adapter_to):
        self._transmit_message(message, adapter_to)

    def _receive_message(self, message: Message):
        self._notify_about_received_message(message)

    def _notify_about_received_message(self, message: Message):
        self.message_received_broadcaster.tell(
            Broadcast(
                sender=self,
                message=message
            )
        )

    def _transmit_message(self, message: Message, adapter_to):
        self._notify_than_we_want_to_transmit_message(message, adapter_to)

    def _notify_than_we_want_to_transmit_message(self, message: Message, adapter_to):
        self.want_to_transmit_message_broadcaster.tell(
            Broadcast(
                sender=self,
                message=AdapterWantsToTransmitMessage(
                    sender=self,
                    adapter_from=self,
                    adapter_to=adapter_to,
                    message=message
                )
            )
        )
