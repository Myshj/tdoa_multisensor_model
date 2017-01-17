# -*- coding: utf-8
import datetime

import gevent
from numpy.linalg import norm

import ActorSystem.Messages
import Messages
from ActorSystem import Actor
from Actors.ASensor import ASensor


class ASignalPropagator(Actor):
    """
    Распространитель сигнала.
    По получении команды на распространение
    1. Определяет время получения сигнала связанными датчиками
    2. В эти определённые времена рассылает датчикам уведомления о получении сигнала.
    """

    def __init__(self, speed_of_sound, source_position):
        """
        Конструктор.
        :param float speed_of_sound: Скорость звука в среде.
        :param numpy.array source_position: Позиция источника звука в формате [x, y, z]
        """
        super(ASignalPropagator, self).__init__()
        self._speed_of_sound = speed_of_sound
        self._sensors = []
        self._source_position = source_position

    def on_message(self, message):
        if isinstance(message, ActorSystem.Messages.AddListener):
            self._sensors.append(message.listener)
        elif isinstance(message, Messages.Propagate):
            when_signal_sent = datetime.datetime.now()
            self._sensors.sort(key=self._sorting_key)
            for signal_listener in self._sensors:
                distance = norm(self._source_position - signal_listener.position)
                delay_in_seconds = distance / self._speed_of_sound

                wake_datetime = when_signal_sent + datetime.timedelta(seconds=delay_in_seconds)

                gevent.spawn(self._send_message_to_listener_after_delay,
                             listener=signal_listener,
                             message=Messages.Receive(self, wake_datetime),
                             delay=delay_in_seconds
                             )

    def _send_message_to_listener_after_delay(self, listener, message, delay):
        gevent.sleep(delay)
        listener.tell(message)

    def _sorting_key(self, listener):
        if not isinstance(listener, ASensor):
            return
        return norm(self._source_position - listener.position)
