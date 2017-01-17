# -*- coding: utf-8
import Messages
from ActorSystem import Actor
from Locator import Locator


class ALocator(Actor):
    """
    Может вычислять позицию источника звука на основании вресени прибытия звуковой волны к датчикам.
    """

    def __init__(self, sensor_positions, speed_of_sound):
        """
        Конструктор.
        :param list(numpy.array) sensor_positions: Список позиций датчиков.
        :param float speed_of_sound: Скорость звука в среде.
        """
        super(ALocator, self).__init__()
        self._locator = Locator(sensor_positions, speed_of_sound)

    def on_message(self, message):
        if isinstance(message, Messages.Locate):
            response = self._locator.locate(message.transit_times)
            print("Response: {0}".format(response))
