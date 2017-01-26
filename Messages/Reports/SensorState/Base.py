from Messages.Reports.Base import Base as ReportMessage
from Actors.WorldRelated.Sensors import Base as Sensor
from ActorSystem import Actor


class Base(ReportMessage):
    """
    Базовый класс для сообщений о состояниях датчиков.
    """

    def __init__(self, sender: Actor, sensor: Sensor):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Sensor sensor: Датчик, о котором идёт речь.
        """
        super().__init__(sender)
        self.sensor = sensor
