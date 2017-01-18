from ActorSystem.Messages import Message
from ActorSystem import Broadcaster
from shapely.geometry import Point
from .Base import Base


class SoundSensor(Base):
    """
    Датчик звука. При получении сигнала уведомляет подписавшихся о факте и времени прибытия сигнала.
    ВНИМАНИЕ! На данный момент, время прибытия сигнала задаётся в сообщении о получении сигнала.
    """

    def __init__(self, position: Point, radius: float, heartbeat_interval: float):
        """
        Конструктор
        :param Point position: Позиция.
        :param float radius: Радиус действия датчика в метрах.
        :param float heartbeat_interval: Интервал между уведомлениями о работоспособности себя в секундах.
        """
        super(SoundSensor, self).__init__()
        self.position = position
        self.signal_received_broadcaster = Broadcaster()
        self.alive_broadcaster = Broadcaster()
        self.heartbeat_interval = heartbeat_interval
        self.radius = radius
        self._state = 'ok'

    def on_message(self, message: Message):
        pass

    def __str__(self):
        return "SoundSensor(position={0})".format(self.position)

    def __repr__(self):
        return "SoundSensor(position={0})".format(self.position)

        # def on_message(self, message):
        #     if isinstance(message, Messages.Receive):
        #         self.signal_received_broadcaster.tell(
        #             ActorSystem.Messages.Broadcast(self, Messages.ReportAboutReceiving(self, message.when, self))
        #         )
        #
        # def on_started(self):
        #     self._start_heartbeat()
        #
        # def _start_heartbeat(self):
        #     gevent.spawn(self._heartbeat_cycle)
        #
        # def _heartbeat_cycle(self):
        #     while self._running and self._state == 'ok':
        #         self.alive_broadcaster.tell(ActorSystem.Messages.Broadcast(self, Messages.Alive(self, actor=self)))
        #         gevent.sleep(self.heartbeat_interval)
