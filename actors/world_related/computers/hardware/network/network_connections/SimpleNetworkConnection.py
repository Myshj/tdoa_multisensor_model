import random

import gevent

from actor_system.broadcasters.messages.listener_actions import Add
from actor_system.messages import Message
from actors.world_related.computers.hardware.network.network_adapters import SimpleNetworkAdapter
from actors.world_related.computers.hardware.network.network_adapters.simple.messages import \
    AdapterWantsToTransmitMessage, ReceiveMessage
from intervals import Interval
from .AbstractNetworkConnection import AbstractNetworkConnection


class SimpleNetworkConnection(AbstractNetworkConnection):
    """
    Простейшее сетевое соединение между сетевыми адаптерами.
    """

    def __init__(
            self,
            adapter_from: SimpleNetworkAdapter,
            adapter_to: SimpleNetworkAdapter,
            possible_latency: Interval
    ):
        super().__init__()
        self._initialize_possible_latency(possible_latency)
        self._initialize_adapters(adapter_from, adapter_to)

    def _initialize_adapters(self, adapter_from: SimpleNetworkAdapter, adapter_to: SimpleNetworkAdapter):
        self._initialize_adapter_from(adapter_from)
        self._initialize_adapter_to(adapter_to)

    def _initialize_adapter_from(self, adapter_from: SimpleNetworkAdapter):
        self.adapter_from = adapter_from

    def _initialize_adapter_to(self, adapter_to: SimpleNetworkAdapter):
        self.adapter_to = adapter_to

    def _initialize_possible_latency(self, possible_latency: Interval):
        self.possible_latency = possible_latency

    def _start_listening(self):
        self.adapter_to.want_to_transmit_message_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )

    def on_message(self, message: Message):
        if isinstance(message, AdapterWantsToTransmitMessage):
            self.on_adapter_wants_to_transmit_message(
                adapter_from=message.adapter_from,
                adapter_to=message.adapter_to,
                message=message.message
            )

    def on_adapter_wants_to_transmit_message(
            self,
            adapter_from: SimpleNetworkAdapter,
            adapter_to: SimpleNetworkAdapter,
            message: Message
    ):
        print('adapter_wants_to_transmit_message')
        if adapter_from == self.adapter_from and adapter_to == self.adapter_to:
            self._transmit_message(message)

    def get_average_latency(self):
        return (self.possible_latency.right_bound.value + self.possible_latency.left_bound.value) / 2

    def _transmit_message(self, message: Message):
        gevent.spawn(self._message_transmission, message=message)

    def _message_transmission(self, message: Message):
        gevent.sleep(
            self._determine_latency_of_transmission() / 1000
        )
        self.adapter_to.tell(
            ReceiveMessage(
                sender=self,
                message=message
            )
        )

    def _determine_latency_of_transmission(self):
        latency = random.randint(self.possible_latency.left_bound.value, self.possible_latency.right_bound.value)

        while not self.possible_latency.contains_value(latency):
            latency = random.randint(self.possible_latency.left_bound.value, self.possible_latency.right_bound.value)

        return latency
