import gevent
from actors.world_related.computers.software.servers.supervisors.sensor_operability import SensorOperabilitySupervisor
from actors.world_related.computers.software.servers.supervisors.tdoa_group import TDOAGroupSupervisor
from actors.world_related.computers.software.sensor_controllers.sound_related.simple import SimpleSoundSensorController
from actors.world_related.computers.software.routers.simple import SimpleRouter
from actors.world_related.computers.messages.actions.software_actions import InstallSoftware
import loaders
import settings
from actors.world_related.computers.software.servers.supervisors.tdoa_group.messages import FormGroups
from actors.world_related.connectors import SoundSourceToPropagatorConnector, \
    SensorSupervisorToTDOAGroupSupervisorConnector
from actors.world_related.signal_related.sound_related.propagators import SoundPropagator
from auxillary import Position

if __name__ == '__main__':
    world_loader = loaders.WorldLoader(
        url=settings.worlds_url,
        credentials=settings.credentials
    )
    worlds = world_loader.load_all()

    interval_bound_loader = loaders.IntervalBoundLoader(
        url=settings.interval_bounds_url,
        credentials=settings.credentials
    )

    interval_bounds = interval_bound_loader.load_all()

    intervals_loader = loaders.IntervalLoader(
        url=settings.intervals_url,
        credentials=settings.credentials,
        interval_bounds=interval_bounds
    )
    intervals = intervals_loader.load_all()

    network_adapters_loader = loaders.NetworkAdapterLoader(
        url=settings.network_adapters_url,
        credentials=settings.credentials,
        worlds=worlds
    )

    network_adapters = network_adapters_loader.load_all()

    network_connections_loader = loaders.NetworkConnectionLoader(
        url=settings.network_connections_url,
        credentials=settings.credentials,
        adapters=network_adapters,
        possible_latencies=intervals
    )

    network_connections = network_connections_loader.load_all()

    sensor_loader = loaders.SensorLoader(
        url=settings.sensors_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sensors = sensor_loader.load_all()

    computers_loader = loaders.ComputerLoader(
        url=settings.computers_url,
        credentials=settings.credentials,
        worlds=worlds,
        sensors=sensors,
        network_adapters=network_adapters
    )

    computers = computers_loader.load_all()

    for computer in computers.values():
        computer.tell(
            InstallSoftware(
                sender=None,
                software=SimpleRouter(
                    computer=computer,
                    known_computers=set(computers.values()),
                    network_connections=set(network_connections.values())
                )
            )
        )
        gevent.sleep()

    gevent.sleep(1)

    sound_source_loader = loaders.SoundSourceLoader(
        url=settings.sound_sources_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sound_sources = sound_source_loader.load_all()

    real_sensors = [sensor for sensor in sensors.values()]

    propagator = SoundPropagator(position=Position(0, 0, 0), world=worlds[1], sensors=real_sensors)
    source_to_propagator_connector = SoundSourceToPropagatorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        source=[v for v in sound_sources.values()][0],
        propagator=propagator
    )

    # group_supervisor = TDOAGroupSupervisor(position=Position(0, 0, 0), world=worlds[1])
    group_supervisors = []
    for computer in computers.values():
        for supervisor in [
            supervisor for supervisor in filter(
                lambda software: isinstance(software, TDOAGroupSupervisor),
                computer.installed_software
            )
            ]:
            group_supervisors.append(supervisor)
    group_supervisor = group_supervisors[0]
    operability_supervisor = SensorOperabilitySupervisor(computer=group_supervisor.computer,
                                                         sensors=real_sensors)
    sensor_supervisor_to_group_supervisor_connector = SensorSupervisorToTDOAGroupSupervisorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        sensor_operability_supervisor=operability_supervisor,
        tdoa_group_supervisor=group_supervisor
    )

    sensor_controllers = set()
    for computer in computers.values():
        for sensor_controller in filter(lambda software: isinstance(software, SimpleSoundSensorController),
                                        computer.installed_software):
            sensor_controllers.add(sensor_controller)

    group_supervisor.tell(FormGroups(sender=None, sensor_controllers=sensor_controllers))

    print('MAUS!')
    while True:
        gevent.sleep(1)
