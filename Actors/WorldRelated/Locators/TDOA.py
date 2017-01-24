# -*- coding: utf-8
from Messages.Actions.Locator import Locate
from .Base import Base
from Locator import Locator


class TDOA(Base):
    """
    Может вычислять позицию источника звука на основании вресени прибытия звуковой волны к датчикам.
    """

    def on_message(self, message):
        if isinstance(message, Locate):
            self.on_locate(time_delays_table=message.time_delays_table)

    def on_locate(self, time_delays_table: dict):
        """
        Выполняется каждый раз при необходимости определения координат.
        :param dict time_delays_table: Словарь в формате: {sensor: time_delay}
        :return:
        """
        self._locate(time_delays_table=time_delays_table)

    def _locate(self, time_delays_table):
        """
        Локализовать объект.
        :param dict time_delays_table: Словарь в формате: {sensor: time_delay}
        :return:
        """
        locator = Locator(
            microphone_positions=map(lambda sensor: sensor.position.as_array(), time_delays_table.keys()),
            speed_of_sound=self.world.speed_of_sound
        )
        print(locator.locate(time_delays_table.values()))
