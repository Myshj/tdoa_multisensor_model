# -*- coding: utf-8
import datetime

import gevent

from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.signal_related.sound_related.propagators.Base import Base
from actors.world_related.signal_related.sound_related.propagators.messages import PropagateSignal
from actors.world_related.signal_related.sound_related.sensors import SoundSensor
from actors.world_related.signal_related.sound_related.sensors.messages import ReceiveSignal as ReceiveSignal
from actors.world_related.signal_related.sound_related.sources import SoundSource
from auxillary import functions
from signals.Sound import Sound as SoundSignal


class SoundPropagator(Base):
    """
    Распространитель звукового сигнала.
    По получении команды на распространение
    1. Определяет время получения сигнала связанными датчиками
    2. В эти определённые времена рассылает датчикам уведомления о получении сигнала.
    """

    def on_message(self, message):
        if isinstance(message, PropagateSignal):
            self.on_propagate_signal(
                signal=message.signal,
                source=message.source,
                sensors=self.sensors
            )

    def on_propagate_signal(self, signal: SoundSignal, source: SoundSource, sensors: list):
        """
        Вызывается каждый раз при необходимости распространения сигнала среди слушателей.
        :param SoundSignal signal: Информация о сигнале.
        :param SoundSource source: Источник сигнала.
        :param list sensors: Датчики.
        :return:
        """
        self._propagate_signal(
            signal=signal,
            source=source,
            sensors=sensors
        )

    def _propagate_signal(self, signal: SoundSignal, source: SoundSource, sensors: list):
        """
        Распространить сигнал среди датчиков.
        :param signal: Сигнал для распространения.
        :param SoundSource source: Источник сигнала.
        :param list sensors: Датчики.
        :return:
        """
        for sensor in sensors:
            self._prepare_signal_sending(
                signal=signal,
                source=source,
                sensor=sensor
            )

    def _prepare_signal_sending(
            self,
            signal: SoundSignal,
            source: SoundSource,
            sensor: SoundSensor
    ):
        """
        Подготовить отправку сигнала к датчику.
        :param SoundSignal signal: Информация о сигнале.
        :param SoundSource source: Источник сигнала.
        :param Actor sensor: Слушатель.
        :return:
        """
        distance = functions.distance_between_positions(source.position, sensor.position)

        if distance > sensor.radius:
            return

        delay_in_seconds = distance / self.world.speed_of_sound

        wake_datetime = signal.when_generated + datetime.timedelta(seconds=delay_in_seconds)
        self._spawn_notifier(
            listener=sensor,
            message=ReceiveSignal(sender=self, signal=signal, when=wake_datetime),
            delay=delay_in_seconds
        )

    def _spawn_notifier(self, listener: Actor, message: ReceiveSignal, delay: float):
        """
        Запустить микропоток для отложенной доставки сообщения.
        :param Actor listener: Слушатель.
        :param Message message: Сообщение для доставки.
        :param float delay: Задержка в секундах.
        :return:
        """
        gevent.spawn(self._notify_listener_after_delay,
                     listener=listener,
                     message=message,
                     delay=delay
                     )

    def _notify_listener_after_delay(self, listener, message, delay):
        """
        Доставить сообщение с задержкой.
        :param Actor listener: Слушатель.
        :param Message message: Сообщение для доставки.
        :param float delay: Задержка в секундах.
        :return:
        """
        gevent.sleep(delay)
        listener.tell(message)
