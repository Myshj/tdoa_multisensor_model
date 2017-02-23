import random
from datetime import datetime

import gevent

from actor_system import Broadcaster
from actor_system.broadcasters.messages import Broadcast
from actors.world_related.signal_related.sound_related.sensors import messages
from actors.world_related.signal_related.sound_related.sensors.Base import Base
from actors.world_related.signal_related.sound_related.sensors.States import States
from actors.worlds import Base as World
from auxillary.Position import Position
from .messages import state_reports


class SoundSensor(Base):
    """
    Датчик звука. При получении сигнала уведомляет подписавшихся о факте и времени прибытия сигнала.
    ВНИМАНИЕ! На данный момент, время прибытия сигнала задаётся в сообщении о получении сигнала.
    """

    def __init__(
            self,
            position: Position,
            world: World,
            radius: float,
            heartbeat_interval: float,
            failure_probability: float,
            state: States):
        """
        Конструктор
        :param World world: Мир, в котором существует датчик.
        :param Position position: Позиция.
        :param float radius: Радиус действия датчика в метрах.
        :param float heartbeat_interval: Интервал между уведомлениями о работоспособности себя в секундах.
        :param float failure_probability: Вероятность поломки датчика каждую секунду.
        :param States state: Состояние датчика.
        """
        super().__init__(
            position=position,
            world=world
        )
        self.signal_received_broadcaster = Broadcaster()
        self.state_broadcaster = Broadcaster()
        self.heartbeat_interval = heartbeat_interval
        self.radius = radius
        self.failure_probability = failure_probability
        self.state = state

    def on_message(self, message):
        if isinstance(message, messages.ReceiveSignal):
            self.on_signal_received(message.signal, message.when)

    def on_started(self):
        self._start_heartbeat()
        self._start_deterioration()

    def on_signal_received(self, signal, when: datetime):
        """
        Выполняется каждый раз при поступлении сигнала.
        :param signal: Информация о сигнале.
        :param datetime when: Когда сигнал был получен.
        :return:
        """
        if self.state == States.Working:
            self._notify_about_received_signal(signal, when)

    def _notify_about_received_signal(self, signal, when: datetime):
        """
        Уведомляет всех заинтересованных о факте получения сигнала.
        :param signal: Информация о сигнале.
        :param datetime when: Когда сигнал был получен.
        :return:
        """
        self.signal_received_broadcaster.tell(
            Broadcast(self, messages.ReportAboutReceivedSignal(self, signal, when, self))
        )

    def _start_heartbeat(self):
        """
        Стартовать периодическое уведомление всех заинтересованных о состоянии себя.
        :return:
        """
        gevent.spawn(self._heartbeat_cycle)

    def _start_deterioration(self):
        """
        Стартовать износ датчика.
        :return:
        """
        gevent.spawn(self._deterioration_cycle)

    def _deterioration_cycle(self):
        """
        Цикл износа датчика.
        :return:
        """
        while self._running and (self.state != States.Broken):
            if self.failure_probability >= random.random():
                self.state = States.Broken
                self._broadcast_broken()
            gevent.sleep(1)

    def _heartbeat_cycle(self):
        """
        Периодически уведомлять всех заинтересованных о работоспособности себя.
        :return:
        """
        while self._running and (self.state == States.Working):
            self._broadcast_alive()
            gevent.sleep(self.heartbeat_interval)

    def _broadcast_alive(self):
        """
        Уведомить всех заинтересованных о том, что датчик в порядке.
        :return:
        """
        self.state_broadcaster.tell(
            Broadcast(
                sender=self,
                message=state_reports.Alive(sender=self, sensor=self)
            )
        )

    def _broadcast_broken(self):
        """
        Уведомить всех заинтересованных о том, что датчик сломан.
        :return:
        """
        self.state_broadcaster.tell(
            Broadcast(
                sender=self,
                message=state_reports.Broken(sender=self, sensor=self)
            )
        )

    def __str__(self):
        return "SoundSensor(position={0})".format(self.position)

    def __repr__(self):
        return "SoundSensor(position={0})".format(self.position)
