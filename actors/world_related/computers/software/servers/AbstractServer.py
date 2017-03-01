from typing import Iterable

from actor_system.broadcasters.messages.listener_actions import Add, Remove
from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.hardware.network.network_adapters.simple import SimpleNetworkAdapter
from actors.world_related.computers.messages.events.hardware_events import *
from actors.world_related.computers.software import AbstractSoftware


class AbstractServer(AbstractSoftware):
    """
    Базовый класс для всех серверов.
    """

    def __init__(self, computer: Computer):
        super().__init__(computer)
        self._initialize_network_adapters(
            filter(lambda hardware: isinstance(hardware, SimpleNetworkAdapter), computer.connected_hardware))
        self._start_listening_to_network_adapters(self.network_adapters)

    def _initialize_network_adapters(self, network_adapters: Iterable):
        self.network_adapters = {
            network_adapter for network_adapter in network_adapters
            }

    def _start_listening_to_network_adapters(self, network_adapters: set):
        # map(self._start_listening_to_network_adapter, network_adapters)
        for network_adapter in network_adapters:
            self._start_listening_to_network_adapter(network_adapter)

    def _start_listening_to_network_adapter(self, network_adapter: SimpleNetworkAdapter):
        network_adapter.message_received_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )

    def _stop_listening_to_network_adapter(self, network_adapter: SimpleNetworkAdapter):
        network_adapter.message_received_broadcaster.tell(
            Remove(
                sender=self,
                actor=self
            )
        )

    def on_message(self, message: Message):
        if isinstance(message, AbstractHardwareEvent):
            self.on_hardware_event(message)

    def on_hardware_event(self, message: AbstractHardwareEvent):
        if isinstance(message, HardwareConnected):
            self.on_hardware_connected(message.hardware)
        elif isinstance(message, HardwareDisconnected):
            self.on_hardware_disconnected(message.hardware)

    def on_hardware_connected(self, hardware):
        if isinstance(hardware, SimpleNetworkAdapter):
            self._start_listening_to_network_adapter(hardware)

    def on_hardware_disconnected(self, hardware):
        if isinstance(hardware, SimpleNetworkAdapter):
            self._stop_listening_to_network_adapter(hardware)
