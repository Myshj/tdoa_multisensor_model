from .Base import Base
from ActorSystem import Actor


class ReconfigurationRequired(Base):
    """
    Сообщение о том, что нужна реконфигурация системы.
    """

    def __init__(self, sender: Actor, sensor_states: dict):
        """
        Конструктор.
        :param sender: Адресант сообщения.
        :param sensor_states: Словарь в формате: {sensor: state}
        """
        super().__init__(sender)
        self.sensor_states = sensor_states
