from datetime import datetime

import gevent

from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators import \
    AbstractEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.sensor_groups.messages import SensorGroupRecognizedSoundSource
from auxillary import Position
from .PositionAndTimeAssumption import PositionAndTimeAssumption


class SimpleEstimatedPositionDeterminator(AbstractEstimatedPositionDeterminator):
    """
    Простейший определитель позиций, использующий потоки сообщений об источниках звука.
    """

    def __init__(
            self,
            computer: Computer,
            max_deviation_in_space: float,
            time_slot: float
    ):
        super().__init__(computer)
        self.max_deviation_in_space = max_deviation_in_space
        self.time_slot = time_slot
        self.table_of_times_and_positions = {}

    def on_message(self, message: Message):
        super().on_message(message)
        if isinstance(message, SensorGroupRecognizedSoundSource):
            self.on_sensor_group_recognized_sound_source(
                estimated_position=message.estimated_position,
                when_recognized=message.when_recognized
            )

    def on_sensor_group_recognized_sound_source(
            self,
            estimated_position: Position,
            when_recognized: datetime
    ):
        self._remember_position_and_time(position=estimated_position, time=when_recognized)

    def _remember_position_and_time(self, position: Position, time: datetime):
        known_assumptions = tuple(
            filter(
                lambda assumption:
                assumption.position.as_point().distance(position.as_point()) <= self.max_deviation_in_space,
                self.table_of_times_and_positions.keys()
            )
        )

        if len(known_assumptions) == 0:
            new_assumption = PositionAndTimeAssumption(position=position, time=time)
            self.table_of_times_and_positions[new_assumption] = set()
            self.table_of_times_and_positions[new_assumption].add(position)
            self._start_waiting_for_new_assumption(new_assumption)
        else:
            for assumption in known_assumptions:
                self.table_of_times_and_positions[assumption].add(position)

    def _start_waiting_for_new_assumption(self, assumption: PositionAndTimeAssumption):
        gevent.spawn(
            self._wait_for_new_assumption,
            assumption=assumption
        )

    def _wait_for_new_assumption(self, assumption: PositionAndTimeAssumption):
        gevent.sleep(self.time_slot)
        self._calculate_estimated_position(assumption)
        self.table_of_times_and_positions.pop(assumption)

    def _calculate_estimated_position(self, assumption: PositionAndTimeAssumption):
        print(
            'Позиция {0} распознана в {1}'.format(assumption.position, datetime.now())
        )
