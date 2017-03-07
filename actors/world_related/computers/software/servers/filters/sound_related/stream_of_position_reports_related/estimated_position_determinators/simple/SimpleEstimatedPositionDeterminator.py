from datetime import datetime

from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators import \
    AbstractEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.sensor_groups.messages import SensorGroupRecognizedSoundSource
from auxillary import Position


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
        self._initialize_table_of_times_and_positions()

    def _initialize_table_of_times_and_positions(self):
        pass

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
        pass
