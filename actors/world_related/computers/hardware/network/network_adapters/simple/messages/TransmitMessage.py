from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers.hardware.network.network_adapters.simple import SimpleNetworkAdapter


class TransmitMessage(Message):
    """
    Сообщение о том, что сетевой адаптер должен передать сообщение другому сетевому адаптеру.
    """

    def __init__(self, sender: Actor, message: Message, adapter_to: SimpleNetworkAdapter):
        super().__init__(sender)
        self.message = message
        self.adapter_to = adapter_to
