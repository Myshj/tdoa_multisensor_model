from actor_system.messages import Message
from actors.world_related.signal_related.sound_related.sensors import Base as Sensor
from actor_system import Actor


class Base(Message):
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
