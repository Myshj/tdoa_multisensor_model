from datetime import datetime, timedelta

import gevent
from numpy.linalg import norm

from actor_system.broadcasters.messages.listener_actions import Add
from actors.world_related.computers import Computer
from actors.world_related.computers.software.locators.tdoa import TDOA
from actors.world_related.computers.software.locators.tdoa.messages import Locate, SoundSourceLocalized
from actors.world_related.computers.software.routers.simple import SimpleRouter
from actors.world_related.computers.software.routers.simple.messages import SendMessageToComputer
from actors.world_related.computers.software.sensor_controllers.sound_related.simple.messages.group_operations import \
    ReportToThisGroup
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators.simple import \
    SimpleEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.sensor_groups import AbstractSensorGroup
from actors.world_related.computers.software.servers.sensor_groups.messages import SensorGroupRecognizedSoundSource
from actors.world_related.computers.software.servers.sensor_groups.messages.position_determinator_operations import \
    AbstractPositionDeterminatorOperation
from actors.world_related.computers.software.servers.sensor_groups.messages.position_determinator_operations import \
    DoNotReportToThisPositionDeterminator
from actors.world_related.computers.software.servers.sensor_groups.messages.position_determinator_operations import \
    ReportToThisPositionDeterminator
from actors.world_related.signal_related.sound_related.sensors import SoundSensor
from actors.world_related.signal_related.sound_related.sensors.messages import ReportAboutReceivedSignal
from auxillary import Position
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

    def __init__(
            self,
            computer: Computer,
            sensor_controllers: list,
            estimated_position_determinators: set
    ):
        """
        Конструктор.
        :param computer: Компьютер, на котором установлена программа.
        :param list(SimpleSoundSensorController) sensor_controllers: Список связанных контроллеров датчиков.
        """
        super().__init__(computer)
        self.sensor_controllers = sensor_controllers
        self.position_determinators = estimated_position_determinators
        self._just_received_signal = False
        self._initialize_locator()
        self._start_listening_to_locator()
        self._initialize_max_wait_time()
        self._listen_for_sensor_signals()

    def on_message(self, message):
        super().on_message(message)
        if isinstance(message, ReportAboutReceivedSignal):
            self.on_sensor_received_signal(
                signal=message.signal,
                when_received=message.when,
                sensor=message.sensor
            )
        elif isinstance(message, SoundSourceLocalized):
            self.on_sound_source_localized(message.estimated_position)
        elif isinstance(message, AbstractPositionDeterminatorOperation):
            self.on_position_determinator_operation(message)

    def on_position_determinator_operation(self, message: AbstractPositionDeterminatorOperation):
        if isinstance(message, ReportToThisPositionDeterminator):
            self.on_report_to_this_position_determinator(message.position_determinator)
        elif isinstance(message, DoNotReportToThisPositionDeterminator):
            self.on_do_not_report_to_this_position_determinator(message.position_determinator)

    def on_report_to_this_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self._add_related_position_determinator(position_determinator)

    def _add_related_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self.position_determinators.add(position_determinator)

    def on_do_not_report_to_this_position_determinator(
            self,
            position_determinator: SimpleEstimatedPositionDeterminator
    ):
        self._remove_related_position_determinator(position_determinator)

    def _remove_related_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self.position_determinators.remove(position_determinator)

    def on_sensor_received_signal(self, signal: Sound, when_received: datetime, sensor: SoundSensor):
        """
        Выполняется каждый раз при получении сигнала одним из связанных датчиков.
        :param Sound signal: Полученный звуковой сигнал.
        :param datetime when_received: Когда сигнал был получен.
        :param SoundSensor sensor: Датчик, получивший сигнал.
        :return:
        """
        if sensor not in map(lambda sensor_controller: sensor_controller.sensor, self.sensor_controllers):
            return
        self._determine_what_to_do_with_signal(
            signal=signal,
            when_received=when_received,
            sensor=sensor
        )

    def on_sound_source_localized(self, estimated_position: Position):
        # print(estimated_position)
        self._notify_position_determinator_about_recognized_sound_source(estimated_position)

    def _notify_position_determinator_about_recognized_sound_source(self, estimated_position: Position):
        router = tuple(
            router for router in
            filter(lambda software: isinstance(software, SimpleRouter), self.computer.installed_software)
        )[0]

        now = datetime.now()

        for position_determinator in self.position_determinators:
            router.tell(
                SendMessageToComputer(
                    sender=self,
                    message=SensorGroupRecognizedSoundSource(
                        sender=self,
                        when_recognized=now,
                        estimated_position=estimated_position
                    ),
                    computer_to=position_determinator.computer
                )
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

            # print('Сигнал был сгенерирован: {0}, будет распознан: {1}'.format(when_received, datetime.now() + timedelta(
            #     seconds=self._max_wait_time)))
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
                    sensor_controller.sensor: (
                        self._last_sensor_report_times[sensor_controller.sensor] - self._last_started_activity_time
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    ).total_seconds()
                    for sensor_controller in self.sensor_controllers
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
        for start_sensor in self.sensor_controllers:
            start_position = start_sensor.sensor.position.as_array()
            for stop_sensor in self.sensor_controllers:
                stop_position = stop_sensor.sensor.position.as_array()
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

    def _start_listening_to_locator(self):
        self.locator.sound_source_localized_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )

    def _listen_for_sensor_signals(self):
        """
        Начать ожидание сигналов от датчиков.
        :return:
        """
        for sensor_controller in self.sensor_controllers:
            sensor_controller.tell(
                ReportToThisGroup(
                    sender=self,
                    sensor_group=self
                )
            )
            # sensor_controller.signal_received_broadcaster.tell(AddListener(self, self))
