import gevent

import Loaders
import settings
from Actors.WorldRelated.SignalPropagators import SoundPropagator
from Actors.WorldRelated.Connectors import SoundSourceToPropagatorConnector, \
    SensorSupervisorToTDOAGroupSupervisorConnector
from Actors.WorldRelated.Supervisors import TDOAGroupSupervisor, SensorOperabilitySupervisor
from Messages.Actions.Supervisors.TDOA import FormGroups
from auxillary import Position

if __name__ == '__main__':
    world_loader = Loaders.WorldLoader(
        url=settings.worlds_url,
        credentials=settings.credentials
    )
    worlds = world_loader.load_all()

    sensor_loader = Loaders.SensorLoader(
        url=settings.sensors_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sensors = sensor_loader.load_all()

    sound_source_loader = Loaders.SoundSourceLoader(
        url=settings.sound_sources_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sound_sources = sound_source_loader.load_all()

    propagator = SoundPropagator(position=Position(0, 0, 0), world=worlds[1], sensors=sensors.values())
    source_to_propagator_connector = SoundSourceToPropagatorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        source=sound_sources[1],
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

    while True:
        gevent.sleep(1)
