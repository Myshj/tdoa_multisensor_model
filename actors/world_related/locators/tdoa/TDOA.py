# -*- coding: utf-8
from actor_system import Broadcaster
from actor_system.broadcasters.messages import Broadcast
from Locator import Locator
from actors.world_related.locators.Base import Base
from actors.world_related.locators.tdoa.messages import Locate, SoundSourceLocalized
from actors.worlds import Base as World
from auxillary import Position


class TDOA(Base):
    """
    Может вычислять позицию источника звука на основании вресени прибытия звуковой волны к датчикам.
    """

    def __init__(self, position: Position, world: World):
        super().__init__(position, world)
        self.sound_source_localized_broadcaster = Broadcaster()

    def on_message(self, message):
        if isinstance(message, Locate):
            self.on_locate(time_delays_table=message.time_delays_table)

    def on_locate(self, time_delays_table: dict):
        """
        Выполняется каждый раз при необходимости определения координат.
        :param dict time_delays_table: Словарь в формате: {sensor: time_delay}
        :return:
        """
        estimated_position = self._locate(time_delays_table=time_delays_table)
        self._notify_that_sound_source_localized(estimated_position)

    def _locate(self, time_delays_table):
        """
        Локализовать объект.
        :param dict time_delays_table: Словарь в формате: {sensor: time_delay}
        :return:
        """
        microphone_positions = []
        time_delays = []
        for sensor in time_delays_table.keys():
            microphone_positions.append(sensor.position.as_array())
            time_delays.append(time_delays_table[sensor])

        locator = Locator(
            microphone_positions=microphone_positions,
            speed_of_sound=self.world.speed_of_sound
        )
        estimated_position = locator.locate(time_delays)
        return Position(
            x=estimated_position[0],
            y=estimated_position[1],
            z=estimated_position[2]
        )

    def _notify_that_sound_source_localized(self, position: Position):
        """
        Уведомить всех заинтересованных о том, что обнаружен источник звука на ожидаемой позиции.
        :param Position position: Ожидаемая позиция источника звука.
        :return:
        """
        print(position)
        self.sound_source_localized_broadcaster.tell(
            Broadcast(
                sender=self,
                message=SoundSourceLocalized(
                    sender=self,
                    estimated_position=position
                )
            )
        )
