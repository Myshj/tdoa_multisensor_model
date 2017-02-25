from actor_system.broadcasters.messages.listener_actions import Add, Remove
from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.messages.events.hardware_events import *
from actors.world_related.computers.software.routers.simple import SimpleRouter
from actors.world_related.computers.software.routers.simple.messages import SendMessageToComputer
from actors.world_related.computers.software.sensor_controllers.sound_related import AbstractSoundSensorController
from actors.world_related.computers.software.sensor_groups import TDOASensorGroup
from actors.world_related.signal_related.sound_related.sensors import SoundSensor
from actors.world_related.signal_related.sound_related.sensors.messages import ReportAboutReceivedSignal
from .messages.group_operations import *


class SimpleSoundSensorController(AbstractSoundSensorController):
    """
    Простейший контроллер звуковых датчиков.
    """

    def __init__(self, computer: Computer):
        super().__init__(computer)
        self._initialize_related_sensors()
        self._listen_to_related_sensors()
        self._initialize_related_groups()
        self._listen_to_hardware_events()

    def on_message(self, message: Message):
        if isinstance(message, ReportAboutReceivedSignal):
            self.on_report_about_received_signal(message)
        elif isinstance(message, AbstractHardwareEvent):
            self.on_hardware_event(message)
        elif isinstance(message, AbstractGroupOperation):
            self.on_group_operation(message)

    def on_group_operation(self, message: AbstractGroupOperation):
        if isinstance(message, ReportToThisGroup):
            self.on_report_to_this_group(message.sensor_group)
        elif isinstance(message, DoNotReportToThisGroup):
            self.on_do_not_report_to_this_group(message.sensor_group)

    def on_report_to_this_group(self, sensor_group: TDOASensorGroup):
        self._add_group_to_related(sensor_group)

    def _add_group_to_related(self, sensor_group: TDOASensorGroup):
        self._related_groups.add(sensor_group)

    def _remove_group_from_related(self, sensor_group: TDOASensorGroup):
        self._related_groups.remove(sensor_group)

    def on_do_not_report_to_this_group(self, sensor_group: TDOASensorGroup):
        self._remove_group_from_related(sensor_group)

    def on_hardware_event(self, message: AbstractHardwareEvent):
        if isinstance(message, HardwareConnected):
            self.on_hardware_connected(message.hardware)
        elif isinstance(message, HardwareDisconnected):
            self.on_hardware_disconnected(message.hardware)

    def on_hardware_connected(self, hardware):
        if isinstance(hardware, SoundSensor):
            self._add_sensor_to_related(hardware)
            self._start_listening_to_sensor(hardware)

    def _add_sensor_to_related(self, sensor: SoundSensor):
        self._related_sensors.add(sensor)

    def _remove_sensor_from_related(self, sensor: SoundSensor):
        self._related_sensors.remove(sensor)

    def on_hardware_disconnected(self, hardware):
        if isinstance(hardware, SoundSensor):
            self._remove_sensor_from_related(hardware)
            self._stop_listening_to_sensor(hardware)

    def on_report_about_received_signal(self, message: ReportAboutReceivedSignal):
        self._notify_related_groups(message)

    def _notify_related_groups(self, message: ReportAboutReceivedSignal):
        for sensor_group in self._related_groups:
            self._notify_related_group(sensor_group, message)

    def _notify_related_group(self, sensor_group: TDOASensorGroup, message: ReportAboutReceivedSignal):
        router = tuple(
            router for router in filter(lambda software: isinstance(software, SimpleRouter), self.computer)
        )[0]

        router.tell(
            SendMessageToComputer(
                sender=self,
                message=message,
                computer_to=sensor_group.computer
            )
        )

    def _initialize_related_groups(self):
        self._related_groups = set()

    def _initialize_related_sensors(self):
        self._related_sensors = {
            sensor for sensor in filter(lambda hardware: isinstance(hardware, SoundSensor),
                                        self.computer.connected_hardware
                                        )
            }

    def _listen_to_related_sensors(self):
        for sensor in self._related_sensors:
            self._start_listening_to_sensor(sensor)

    def _start_listening_to_sensor(self, sensor: SoundSensor):
        sensor.signal_received_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )

    def _stop_listening_to_sensor(self, sensor: SoundSensor):
        sensor.signal_received_broadcaster.tell(
            Remove(
                sender=self,
                actor=self
            )
        )

    def _listen_to_hardware_events(self):
        self.computer.hardware_events_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )
