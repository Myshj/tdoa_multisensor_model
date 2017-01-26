# -*- coding: utf-8
import gevent
import numpy

import ActorSystem.Messages
import Messages
from ActorSystem import Actor
from Actors.WorldRelated.CombinationCalculators.TDOACombinationCalculator import TDOACombinationCalculator
from Actors.WorldRelated.SensorGroups.TDOASensorGroup import TDOASensorGroup
from Actors.WorldRelated.SignalPropagators import SoundPropagator
from Actors.WorldRelated.SignalSources import SoundSource
from Actors.WorldRelated.Supervisors.SensorOperabilitySupervisor import SensorOperabilitySupervisor


class AModel(Actor):
    """
    Модель системы, состоящей из нескольких звуковых датчиков, объединенных в группы, и одного источника звука.
    """

    def __init__(self, sensors, sensor_groups, speed_of_sound):
        """
        Конструктор.
        :param list(SoundSensor) sensors: Список акторов-датчиков.
        :param list(TDOASensorGroup)sensor_groups: Список акторов-групп датчиков.
        :param float speed_of_sound: Скорость звука в среде.
        """
        super(AModel, self).__init__()
        group_former = TDOACombinationCalculator()
        self._speed_of_sound = speed_of_sound

        self._sensor_actors = sensors

        group_former.tell(Messages.FormGroups(self, sensors))

        gevent.sleep(1)

        self._initialize_sensor_supervisor()
        self._initialize_sensor_groups(sensor_groups)

        self._initialize_signal_propagator()
        self._initialize_signal_source()

        self.ended = False

    def on_message(self, message):
        pass

    def _initialize_sensor_groups(self, sensor_groups):
        self._sensor_groups = {
            sensor_group_key: TDOASensorGroup(
                sensors=[
                    self._sensor_actors[sensor_actor_key] for sensor_actor_key in sensor_groups[sensor_group_key]
                    ],
                speed_of_sound=self._speed_of_sound,
            ) for sensor_group_key in sensor_groups.keys()
            }

    def _initialize_signal_propagator(self):
        self._signal_propagator = SoundPropagator(speed_of_sound=self._speed_of_sound,
                                                  source_position=AModel.list_to_vector((7, 7, 0)))
        for sensor in self._sensor_actors:
            self._signal_propagator.tell(ActorSystem.Messages.AddListener(self, self._sensor_actors[sensor]))

    def _initialize_signal_source(self):
        self._signal_source = SoundSource(position=AModel.list_to_vector((7, 7, 0)),
                                          signal_propagator=self._signal_propagator)
        self._signal_source.tell(Messages.GenerateSignal(self))

    def _initialize_sensor_supervisor(self):
        self._sensor_supervisor = SensorOperabilitySupervisor(self._sensor_actors)

    @staticmethod
    def list_to_vector(list):
        return numpy.array([
            list[0],
            list[1],
            list[2]
        ])

    @staticmethod
    def vector_to_list(vector):
        return [
            vector[0],
            vector[1],
            vector[2]
        ]
