from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers.hardware.network.network_adapters.simple import SimpleNetworkAdapter


class AdapterWantsToTransmitMessage(Message):
    """
    Сообщение о том, что сетевой адаптер хочет передать сообщение.
    """

    def __init__(
            self,
            sender: Actor,
            adapter_from: SimpleNetworkAdapter,
            adapter_to: SimpleNetworkAdapter,
            message: Message
    ):
        super().__init__(sender)
        self.adapter_from = adapter_from
        self.adapter_to = adapter_to
        self.message = message
