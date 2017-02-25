from auxillary import functions
from .AbstractLoader import AbstractLoader
from actors.world_related.computers.hardware.network.network_connections import SimpleNetworkConnection


class NetworkConnectionLoader(AbstractLoader):
    """
    Загружает сетевые соединения.
    """

    def __init__(
            self,
            url: str,
            credentials: tuple,
            adapters: dict,
            possible_latencies: dict
    ):
        super().__init__(url, credentials)
        self.adapters = adapters
        self.possible_latencies = possible_latencies

    def _restore_actor(self, actor_info: dict):
        """

        :param actor_info: {
        'id': int,
        'adapter_from': str,
        'adapter_to': str,
        'possible_latency': str
        }
        :return:
        """
        adapter_from = self.adapters[
            functions.get_json_from_server(actor_info['adapter_from'], self._credentials)['id']
        ]
        adapter_to = self.adapters[functions.get_json_from_server(actor_info['adapter_to'], self._credentials)['id']]
        possible_latency = self.possible_latencies[
            functions.get_json_from_server(actor_info['possible_latency'], self._credentials)['id']
        ]

        return SimpleNetworkConnection(
            adapter_from=adapter_from,
            adapter_to=adapter_to,
            possible_latency=possible_latency
        )
