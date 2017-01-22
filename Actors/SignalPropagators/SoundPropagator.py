# -*- coding: utf-8
import datetime

import gevent
from numpy.linalg import norm
from .Base import Base
from ActorSystem import Actor
from ActorSystem.Messages import Message
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from ActorSystem.Messages.ActorActions.ListenerActions import Remove as RemoveListener
from Actors.WorldRelated.Sensors import SoundSensor
from Messages.Actions.Signal import Propagate as PropagateSignal
from Messages.Actions.Signal import Receive as ReceiveSignal
from Signals.Sound import Sound as SoundSignal
from auxillary import Position
from auxillary import functions


class SoundPropagator(Base):
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
        :param Position source_position: Позиция источника звука в формате [x, y, z]
        """
        super().__init__()
        self._speed_of_sound = speed_of_sound
        self._sensors = []
        self._source_position = source_position

    def on_message(self, message):
        if isinstance(message, AddListener):
            self._add_listener(message.actor)
        elif isinstance(message, RemoveListener):
            self._remove_listener(message.actor)
        elif isinstance(message, PropagateSignal):
            self.on_propagate_signal(message.signal)

    def on_propagate_signal(self, signal: SoundSignal):
        """
        Вызывается каждый раз при необходимости распространения сигнала среди слушателей.
        :param SoundSignal signal: Информация о сигнале.
        :return:
        """
        self._propagate_signal(signal)

    def _propagate_signal(self, signal: SoundSignal):
        """
        Распространить сигнал среди датчиков.
        :param signal: Сигнал для распространения.
        :return:
        """
        when_signal_generated = signal.when_generated
        self._sensors.sort(key=self._sorting_key)
        for signal_listener in self._sensors:
            self._prepare_signal_sending(
                when_signal_generated=when_signal_generated,
                signal=signal,
                signal_listener=signal_listener
            )

    def _add_listener(self, listener: Actor):
        """
        Добавить датчик в список слушателейю
        :param Actor listener: Датчик.
        :return:
        """
        self._sensors.append(listener)

    def _remove_listener(self, listener: Actor):
        """
        Убрать датчик из списка слушателей.
        :param Actor listener: Датчик.
        :return:
        """
        self._sensors.remove(listener)

    def _prepare_signal_sending(
            self,
            when_signal_generated: datetime.datetime,
            signal: SoundSignal,
            signal_listener: SoundSensor
    ):
        """
        Подготовить отправку сигнала к датчику.
        :param datetime when_signal_generated: Когда сигнал был сгенерирован.
        :param SoundSignal signal: Информация о сигнале.
        :param Actor signal_listener: Слушатель.
        :return:
        """
        distance = functions.distance_between_positions(self._source_position, signal_listener)
        delay_in_seconds = distance / self._speed_of_sound

        wake_datetime = when_signal_generated + datetime.timedelta(seconds=delay_in_seconds)
        self._spawn_notifier(
            listener=signal_listener,
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

    def _sorting_key(self, listener):
        if not isinstance(listener, SoundSensor):
            return
        return norm(self._source_position.as_array() - listener.position.as_array())
