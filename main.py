import gevent

import Loaders
import settings
from Messages.Actions.CombinationCalculator import CalculateCombinations
from Actors.WorldRelated.CombinationCalculators import TDOACombinationCalculator
from Actors.WorldRelated.SignalPropagators import SoundPropagator
from Actors.WorldRelated.Connectors import SoundSourceToPropagatorConnector
from Actors.WorldRelated.SensorGroups import TDOASensorGroup
from Actors.WorldRelated.Supervisors import TDOAGroupSupervisor
from Actors.WorldRelated.Connectors import TDOACombinationCalculatorToGroupSupervisorConnector
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

    combination_calculator = TDOACombinationCalculator(position=Position(0, 0, 0), world=worlds[1])
    group_supervisor = TDOAGroupSupervisor(position=Position(0, 0, 0), world=worlds[1])
    combination_calculator_to_group_supervisor_connector = TDOACombinationCalculatorToGroupSupervisorConnector(
        position=Position(0, 0, 0),
        world=worlds[1],
        combination_calculator=combination_calculator,
        group_supervisor=group_supervisor
    )

    combination_calculator.tell(
        CalculateCombinations(sender=None, sensors=sensors.values())
    )

    group = TDOASensorGroup(
        position=Position(0, 0, 0),
        world=worlds[1],
        sensors=[sensors[2], sensors[4], sensors[6], sensors[8], sensors[10]]
    )

    while True:
        gevent.sleep(1)
