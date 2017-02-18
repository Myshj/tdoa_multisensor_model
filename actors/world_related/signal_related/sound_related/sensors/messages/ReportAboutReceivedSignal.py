from datetime import datetime

from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.signal_related.sound_related.sensors import SoundSensor


class ReportAboutReceivedSignal(Message):
    """
    Сообщение о том, что некий сенсор получил сигнал.
    """

    def __init__(self, sender: Actor, signal, when: datetime, sensor: SoundSensor):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param signal: Сигнал, о котором идёт речь.
        :param datetime when: Когда сигнал был получен.
        :param SoundSensor sensor: Кем сигнал был получен.
        """
        super().__init__(sender)
        self.signal = signal
        self.when = when
        self.sensor = sensor
