from datetime import datetime

import gevent

import Messages
from ActorSystem import Broadcaster
from ActorSystem.Messages import Broadcast
from Actors.Worlds import Base as World
from auxillary.Position import Position
from .Base import Base


class SoundSensor(Base):
    """
    Датчик звука. При получении сигнала уведомляет подписавшихся о факте и времени прибытия сигнала.
    ВНИМАНИЕ! На данный момент, время прибытия сигнала задаётся в сообщении о получении сигнала.
    """

    def __init__(self, position: Position, world: World, radius: float, heartbeat_interval: float, state: str):
        """
        Конструктор
        :param World world: Мир, в котором существует датчик.
        :param Position position: Позиция.
        :param float radius: Радиус действия датчика в метрах.
        :param float heartbeat_interval: Интервал между уведомлениями о работоспособности себя в секундах.
        """
        super().__init__(
            position=position,
            world=world
        )
        self.signal_received_broadcaster = Broadcaster()
        self.alive_broadcaster = Broadcaster()
        self.heartbeat_interval = heartbeat_interval
        self.radius = radius
        self.state = state

    def on_message(self, message):
        if isinstance(message, Messages.Actions.Signal.Receive):
            self.on_signal_received(message.signal, message.when)

    def on_started(self):
        self._start_heartbeat()

    def on_signal_received(self, signal, when: datetime):
        """
        Выполняется каждый раз при поступлении сигнала.
        :param signal: Информация о сигнале.
        :param datetime when: Когда сигнал был получен.
        :return:
        """
        self._notify_about_received_signaal(signal, when)

    def _notify_about_received_signaal(self, signal, when: datetime):
        """
        Уведомляет всех заинтересованных о факте получения сигнала.
        :param signal: Информация о сигнале.
        :param datetime when: Когда сигнал был получен.
        :return:
        """
        self.signal_received_broadcaster.tell(
            Broadcast(self, Messages.Actions.Signal.ReportAboutReceiving(self, signal, when, self))
        )

    def _start_heartbeat(self):
        """
        Стартовать периодическое уведомление всех заинтересованных о состоянии себя.
        :return:
        """
        gevent.spawn(self._heartbeat_cycle)

    def _heartbeat_cycle(self):
        """
        Периодически уведомлять всех заинтересованных о состоянии себя.
        :return:
        """
        while self._running and self.state == 'working':
            self.alive_broadcaster.tell(Broadcast(self, Messages.ActorReports.Alive(self, actor=self)))
            gevent.sleep(self.heartbeat_interval)

    def __str__(self):
        return "SoundSensor(position={0})".format(self.position)

    def __repr__(self):
        return "SoundSensor(position={0})".format(self.position)
