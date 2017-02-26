from .WorldRelatedObjectLoader import WorldRelatedObjectLoader
from auxillary import functions
from actors.world_related.computers.messages.actions.hardware_actions import ConnectHardware
from actors.world_related.computers.messages.actions.software_actions import InstallSoftware
from actors.world_related.computers import Computer
from auxillary import Position
import gevent
from actors.world_related.computers.software.sensor_controllers.sound_related.simple import SimpleSoundSensorController
from actors.world_related.computers.software.supervisors.tdoa_group import TDOAGroupSupervisor


class ComputerLoader(WorldRelatedObjectLoader):
    """
    Загружает компьютеры.
    """

    def __init__(
            self,
            url: str,
            credentials: tuple,
            worlds: dict,
            sensors: dict,
            network_adapters: dict
    ):
        super().__init__(url, credentials, worlds)
        self.sensors = sensors
        self.network_adapters = network_adapters

    def _restore_actor(self, actor_info: dict):
        """

        :param actor_info: {
        'id': int,
        'sensors': list(str),
        'network_adapters': list(str),
        'position': str,
        'world': str,
        'is_active_sensor_controller': bool,
        'is_active_tdoa_controller': bool
        }
        :return:
        """
        # position = self.positions[functions.get_json_from_server(actor_info['position'], self._credentials)['id']]
        p = functions.get_json_from_server(actor_info['position'], self._credentials)
        world = self.worlds[functions.get_json_from_server(actor_info['world'], self._credentials)['id']]
        sensors = [
            self.sensors[functions.get_json_from_server(sensor_url, self._credentials)['id']]
            for sensor_url in actor_info['sensors']
            ]

        network_adapters = [
            self.network_adapters[functions.get_json_from_server(network_adapter_url, self._credentials)['id']]
            for network_adapter_url in actor_info['network_adapters']
            ]

        computer = Computer(
            position=Position(p['x'], p['y'], p['z']),
            world=world
        )

        connected_hardware = network_adapters + sensors

        for hardware in connected_hardware:
            computer.tell(
                ConnectHardware(
                    sender=None,
                    hardware=hardware
                )
            )

        if actor_info['is_active_sensor_controller']:
            computer.tell(
                InstallSoftware(
                    sender=None,
                    software=SimpleSoundSensorController(computer)
                )
            )
        if actor_info['is_active_tdoa_controller']:
            computer.tell(
                InstallSoftware(
                    sender=None,
                    software=TDOAGroupSupervisor(computer)
                )
            )

        return computer
