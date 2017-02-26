from datetime import datetime

import gevent
from actors.world_related.computers.software.locators.tdoa import TDOA
from numpy.linalg import norm
from actors.world_related.computers import Computer
from actor_system.broadcasters.messages.listener_actions import Add as AddListener
from actors.world_related.computers.software.locators.tdoa.messages import Locate
from actors.world_related.computers.software.sensor_groups import AbstractSensorGroup
from actors.world_related.signal_related.sound_related.sensors import SoundSensor
from actors.world_related.signal_related.sound_related.sensors.messages import ReportAboutReceivedSignal
from signals import Sound


class TDOASensorGroup(AbstractSensorGroup):
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

    def __init__(self, computer: Computer, sensors: list):
        """
        Конструктор.
        :param computer: Компьютер, на котором установлена программа.
        :param list(SoundSensor) sensors: Список связанных датчиков.
        """
        super().__init__(computer)
        self.sensors = sensors
        self._just_received_signal = False
        self._initialize_locator()
        self._initialize_max_wait_time()
        self._listen_for_sensor_signals()

    def on_message(self, message):
        if isinstance(message, ReportAboutReceivedSignal):
            self.on_sensor_received_signal(
                signal=message.signal,
                when_received=message.when,
                sensor=message.sensor
            )

    def on_sensor_received_signal(self, signal: Sound, when_received: datetime, sensor: SoundSensor):
        """
        Выполняется каждый раз при получении сигнала одним из связанных датчиков.
        :param Sound signal: Полученный звуковой сигнал.
        :param datetime when_received: Когда сигнал был получен.
        :param SoundSensor sensor: Датчик, получивший сигнал.
        :return:
        """
        self._determine_what_to_do_with_signal(
            signal=signal,
            when_received=when_received,
            sensor=sensor
        )

    def _determine_what_to_do_with_signal(self, signal: Sound, when_received: datetime, sensor: SoundSensor):
        """
        В группе был зафиксирован сигнал. Нужно выяснить, что нам с ним делать.
        :param Sound signal: Полученный звуковой сигнал.
        :param datetime when_received: Когда сигнал был получен.
        :param SoundSensor sensor: Датчик, получивший сигнал.
        :return:
        """
        if not self._just_received_signal:
            self._last_started_activity_time = when_received
            self._last_sensor_report_times = {}
            self._just_received_signal = True
            gevent.spawn(self._wait_for_max_wait_time)
        self._last_sensor_report_times[sensor] = when_received

    def _wait_for_max_wait_time(self):
        """
        Ждать максимальное время ожидании.
        После окончания ожидания вызвать соответствующее событие.
        :return:
        """
        gevent.sleep(self._max_wait_time)
        self._on_wait_time_exceed()

    def _on_wait_time_exceed(self):
        """
        Выполняется каждый раз после истечения максимального времени ожидания.
        :return:
        """
        if self._all_sensors_reported():
            self._activate_locator()
        self._just_received_signal = False

    def _activate_locator(self):
        """
        Выдача команды локатору на обнаружение объекта.
        :return:
        """
        self.locator.tell(
            Locate(
                sender=self,
                time_delays_table={
                    sensor: (
                        self._last_sensor_report_times[sensor] - self._last_started_activity_time
                    ).total_seconds()
                    for sensor in self.sensors
                    }
            )
        )

    def _all_sensors_reported(self):
        """
        Все ли датчики зафиксировали сигнал?
        :return: True, если все датчики зафиксировали сигнал. False в другом случае.
        """
        return len(self._last_sensor_report_times) >= 5

    def _initialize_max_wait_time(self):
        """
        Инициализация максимального времени ожидания.
        :return:
        """
        max_distance = 0.0
        for start_sensor in self.sensors:
            start_position = start_sensor.position.as_array()
            for stop_sensor in self.sensors:
                stop_position = stop_sensor.position.as_array()
                distance = norm(start_position - stop_position)
                max_distance = max([max_distance, distance])
        self._max_wait_time = (
                                  max_distance / self.computer.world.speed_of_sound) * TDOASensorGroup.multiplier_for_max_wait_time + 0.5

    def _initialize_locator(self):
        """
        Инициализация локатора.
        :return:
        """
        self.locator = TDOA(
            position=None,
            world=self.computer.world
        )

    def _listen_for_sensor_signals(self):
        """
        Начать ожидание сигналов от датчиков.
        :return:
        """
        for sensor_actor in self.sensors:
            sensor_actor.signal_received_broadcaster.tell(AddListener(self, self))
