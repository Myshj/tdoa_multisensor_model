from .WorldRelatedObjectLoader import WorldRelatedObjectLoader
from auxillary import functions
from auxillary import Position
from actors.world_related.computers.hardware.network.network_adapters.simple import SimpleNetworkAdapter


class NetworkAdapterLoader(WorldRelatedObjectLoader):
    """
    Загружает сетевые адаптеры.
    """

    def _restore_actor(self, actor_info: dict):
        p = functions.get_json_from_server(actor_info['position'], self._credentials)
        world = self.worlds[functions.get_json_from_server(actor_info['world'], self._credentials)['id']]

        return SimpleNetworkAdapter(
            position=Position(p['x'], p['y'], p['z']),
            world=world
        )
