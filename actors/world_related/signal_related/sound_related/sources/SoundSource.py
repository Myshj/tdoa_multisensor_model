# -*- coding: utf-8
from datetime import datetime

import gevent

from . import messages
from ActorSystem import Broadcaster
from ActorSystem.Messages import Broadcast
from Signals import Sound as SoundSignal
from actors.world_related.signal_related.sound_related.sources.Base import Base
from actors.worlds import Base as World
from auxillary.Position import Position


class SoundSource(Base):
    """
    Источник звукового сигнала.
    """

    def __init__(self, position: Position, world: World, interval: float, state: str):
        """
        Конструктор.
        :param Position position: Позиция.
        :param World world: Мир, в котором существует датчик.
        :param float interval: Интервал в секундах между генерациями сигнала.
        :param sre state: Текущее состояние.
        """
        super().__init__(
            position=position,
            world=world
        )
        self.interval = interval
        self.state = state

        self.signal_generated_broadcaster = Broadcaster()

    def on_message(self, message):
        if isinstance(message, messages.GenerateSignal):
            self.on_generate_signal()

    def on_generate_signal(self):
        """
        Вызывается каждый раз, когда требуется сгенерировать сигнал.
        :return:
        """

        self._notify_about_generated_signal(
            signal=self._generate_signal()
        )

    def on_started(self):
        self._start_periodic_generating()

    def _start_periodic_generating(self):
        """
        Старт периодического генерирования сигнала.
        :return:
        """
        gevent.spawn(self._periodic_generating)

    def _periodic_generating(self):
        """
        Цикл периодического генерирования сигнала.
        :return:
        """

        while self._running and self.state == 'working':
            self.on_generate_signal()
            gevent.sleep(self.interval)

    def _notify_about_generated_signal(self, signal):
        """
        Уведомляет всех заинтересованных о факте генерации сигнала.
        :param signal: Информация о сигнале.
        :param when: Время генерации сигнала.
        :return:
        """
        self.signal_generated_broadcaster.tell(
            Broadcast(
                sender=self,
                message=messages.SignalGenerated(
                    sender=self,
                    signal=signal,
                    source=self
                ))
        )

    def _generate_signal(self):
        """
        Генерирует сигнал.
        :return:
        """
        return SoundSignal(when_generated=datetime.now())

    def __str__(self):
        return "SoundSource(position={0})".format(self.position)

    def __repr__(self):
        return "SoundSource(position={0})".format(self.position)
