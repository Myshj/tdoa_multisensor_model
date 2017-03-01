from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.hardware.network.network_adapters import SimpleNetworkAdapter
from actors.world_related.computers.hardware.network.network_adapters.simple.messages import TransmitMessage
from actors.world_related.computers.software.routers import AbstractRouter
from .messages import SendMessageToComputer


class SimpleRouter(AbstractRouter):
    """
    Простейшее маршрутизирующее ПО.
    """

    def __init__(self, computer: Computer, known_computers: set, network_connections: set):
        super().__init__(computer)
        self.known_computers = known_computers
        self.network_connections = network_connections

    def on_message(self, message: Message):
        if isinstance(message, SendMessageToComputer):
            self.on_send_message_to_computer(message=message.message, computer_to=message.computer_to)

    def on_send_message_to_computer(self, message: Message, computer_to: Computer):
        if self.is_computer_known(computer_to):
            self._send_message_to_computer(message, computer_to)

    def is_computer_known(self, computer: Computer):
        return computer in self.known_computers

    def _send_message_to_computer(self, message: Message, computer_to: Computer):
        our_network_adapters = set(filter(
            lambda hardware: isinstance(hardware, SimpleNetworkAdapter),
            self.computer.connected_hardware
        ))

        remote_network_adapters = set(filter(
            lambda hardware: isinstance(hardware, SimpleNetworkAdapter),
            computer_to.connected_hardware
        ))

        possible_connections = [connection for connection in filter(
            lambda network_connection:
            network_connection.adapter_from in our_network_adapters and
            network_connection.adapter_to in remote_network_adapters,
            self.network_connections
        )]

        possible_connections.sort(
            key=lambda connection: connection.get_average_latency()
        )

        possible_connections[0].adapter_from.tell(
            TransmitMessage(
                sender=message.sender,
                message=message,
                adapter_to=possible_connections[0].adapter_to
            )
        )
