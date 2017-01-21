# -*- coding: utf-8
import gevent
import Messages
from datetime import datetime
from ActorSystem import Broadcaster
from ActorSystem.Messages import Broadcast
from .Base import Base
from shapely.geometry import Point


class SoundSource(Base):
    """
    Источник звукового сигнала.
    """

    def __init__(self, position: Point, interval: float, state: str):
        """
        Конструктор.
        :param Point position: Позиция.
        :param float interval: Интервал в секундах между генерациями сигнала.
        :param sre state: Текущее состояние.
        """
        super().__init__()
        self.position = position
        self.interval = interval
        self.state = state

        self.signal_generated_broadcaster = Broadcaster()

    def on_message(self, message):
        if isinstance(message, Messages.Actions.SignalSource.GenerateSignal):
            self.on_generate_signal()

    def on_generate_signal(self):
        """
        Вызывается каждый раз, когда требуется сгенерировать сигнал.
        :return:
        """

        self._notify_about_generated_signal(
            signal=self._generate_signal(),
            when=datetime.now()
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

    def _notify_about_generated_signal(self, signal, when: datetime):
        """
        Уведомляет всех заинтересованных о факте генерации сигнала.
        :param signal: Информация о сигнале.
        :param when: Время генерации сигнала.
        :return:
        """
        self.signal_generated_broadcaster.tell(
            Broadcast(
                sender=self,
                message=Messages.Actions.SignalSource.SignalGenerated(
                    sender=self,
                    signal=signal,
                    source=self,
                    when=when
                ))
        )

    def _generate_signal(self):
        """
        Генерирует сигнал.
        :return:
        """
        return None

    def __str__(self):
        return "SoundSource(position={0})".format(self.position)

    def __repr__(self):
        return "SoundSource(position={0})".format(self.position)
