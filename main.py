import gevent

import loaders
import settings
from actors.world_related.computers.software.supervisors.sensor_operability import SensorOperabilitySupervisor
from actors.world_related.computers.software.supervisors.tdoa_group import TDOAGroupSupervisor
from actors.world_related.computers.software.supervisors.tdoa_group.messages import FormGroups
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

    sound_source_loader = loaders.SoundSourceLoader(
        url=settings.sound_sources_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sound_sources = sound_source_loader.load_all()

    propagator = SoundPropagator(position=Position(0, 0, 0), world=worlds[1], sensors=sensors.values())
    source_to_propagator_connector = SoundSourceToPropagatorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        source=[v for v in sound_sources.values()][0],
        propagator=propagator
    )

    group_supervisor = TDOAGroupSupervisor(position=Position(0, 0, 0), world=worlds[1])
    operability_supervisor = SensorOperabilitySupervisor(position=Position(0, 0, 0), world=worlds[1],
                                                         sensors=sensors.values())
    sensor_supervisor_to_group_supervisor_connector = SensorSupervisorToTDOAGroupSupervisorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        sensor_operability_supervisor=operability_supervisor,
        tdoa_group_supervisor=group_supervisor
    )
    group_supervisor.tell(FormGroups(sender=None, sensors=sensors.values()))

    print('MAUS!')
    while True:
        gevent.sleep(1)
