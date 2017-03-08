from actors.world_related.computers import Computer
from actors.world_related.computers.messages.actions.hardware_actions import ConnectHardware
from actors.world_related.computers.messages.actions.software_actions import InstallSoftware
from actors.world_related.computers.software.sensor_controllers.sound_related.simple import SimpleSoundSensorController
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators.simple import \
    SimpleEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.supervisors.tdoa_group import TDOAGroupSupervisor
from auxillary import Position
from auxillary import functions
from .WorldRelatedObjectLoader import WorldRelatedObjectLoader
import gevent


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
        'is_active_tdoa_controller': bool,
        'is_active_position_determinator': bool
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
            gevent.sleep()

        if actor_info['is_active_sensor_controller']:
            for sensor in sensors:
                computer.tell(
                    InstallSoftware(
                        sender=None,
                        software=SimpleSoundSensorController(computer, sensor)
                    )
                )
            gevent.sleep()

        if actor_info['is_active_tdoa_controller']:
            computer.tell(
                InstallSoftware(
                    sender=None,
                    software=TDOAGroupSupervisor(computer)
                )
            )
            gevent.sleep()

        if actor_info['is_active_position_determinator']:
            computer.tell(
                InstallSoftware(
                    sender=None,
                    software=SimpleEstimatedPositionDeterminator(
                        computer=computer,
                        max_deviation_in_space=20,
                        time_slot=1
                    )
                )
            )
            gevent.sleep()

        return computer
