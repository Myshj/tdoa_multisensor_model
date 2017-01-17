from datetime import datetime

from ActorSystem import Actor
from Actors.ASensor import ASensor
from .Base import Base


class ReportAboutReceiving(Base):
    """
    Сообщение о том, что некий сенсор получил сигнал.
    """

    def __init__(self, sender: Actor, signal, when: datetime, sensor: ASensor):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param signal: Сигнал, о котором идёт речь.
        :param datetime when: Когда сигнал был получен.
        :param ASensor sensor: Кем сигнал был получен.
        """
        super().__init__(sender, signal)
        self.when = when
        self.sensor = sensor
