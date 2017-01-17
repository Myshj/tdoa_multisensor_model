import gevent
from numpy.linalg import norm

import ActorSystem.Messages
import Messages
from ActorSystem import Actor
from Actors.ALocator import ALocator


class ASensorGroup(Actor):
    """
    Группа звуковых датчиков.
    Может находиться в состояниях:
    1. ПОКОЙ
    2. ВНИМАНИЕ
    При получении уведомления от одного из датчиков происходит следующее:
    1. Если система в состоянии ПОКОЙ, то
    1.0. Перейти в состояние ВНИМАНИЕ
    1.1. Запомнить время прибытия уведомления.
    1.2. Ждать некоторое время уведомлений от всех датчиков
    1.3. По истечении времени, посмотреть, все ли датчики получили сигналы.
    1.3.1. Если все, то отправить команду на вычисление позиции источника звука
    1.4. Перейти в состояние ПОКОЙ
    2. Если система в состоянии ВНИМАНИЕ, то
    2.1. Запомнить время прибытия уведомления.
    """
    multiplier_for_max_wait_time = 1.1

    def __init__(self, sensors_actors, speed_of_sound):
        """
        Конструктор.
        :param list(ASensor) sensors_actors: Список связанных акторов-датчиков.
        :param float speed_of_sound: Скорость звука в среде.
        """
        super(ASensorGroup, self).__init__()
        self._speed_of_sound = speed_of_sound
        self._sensors_actors = sensors_actors
        self._just_received_signal = False
        self._initialize_locator()
        self._initialize_max_wait_time()
        self._listen_for_sensor_signals()

    def on_message(self, message):
        if isinstance(message, Messages.ReportAboutReceiving):
            self._on_received_signal(
                when_received=message.when,
                sender=message.sensor
            )

    def _on_received_signal(self, when_received, sender):
        if not self._just_received_signal:
            self._last_started_activity_time = when_received
            self._last_sensor_report_times = {}
            self._just_received_signal = True
            gevent.spawn(self._wait_for_max_wait_time)
        self._last_sensor_report_times[sender] = when_received

    def _wait_for_max_wait_time(self):
        gevent.sleep(self._max_wait_time)
        self._on_wait_time_exceed()

    def _on_wait_time_exceed(self):
        if len(self._last_sensor_report_times) == 5:
            self._locator_actor.tell(
                Messages.Locate(
                    self,
                    transit_times=[
                        (self._last_sensor_report_times[
                             sensor] - self._last_started_activity_time).total_seconds()
                        for sensor in self._sensors_actors
                        ]
                )
            )
        self._just_received_signal = False

    def _initialize_max_wait_time(self):
        max_distance = 0.0
        for start_sensor in self._sensors_actors:
            start_position = start_sensor.position
            for stop_sensor in self._sensors_actors:
                stop_position = stop_sensor.position
                distance = norm(start_position - stop_position)
                max_distance = max([max_distance, distance])
        self._max_wait_time = (max_distance / self._speed_of_sound) * ASensorGroup.multiplier_for_max_wait_time

    def _initialize_locator(self):
        self._locator_actor = ALocator(
            sensor_positions=[sensor_actor.position for sensor_actor in self._sensors_actors],
            speed_of_sound=self._speed_of_sound
        )

    def _listen_for_sensor_signals(self):
        for sensor_actor in self._sensors_actors:
            sensor_actor.tell(ActorSystem.Messages.AddListener(self, self))
