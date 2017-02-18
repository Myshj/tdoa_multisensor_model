from .Base import Base
from ActorSystem import Actor


class Locate(Base):
    """
    Сообщение о том, что нужно вычислить положение объекта на основании задержек прихода сигнала от него.
    """

    def __init__(self, sender: Actor, time_delays_table: dict):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param dict time_delays_table: Словарь в формате: {sensor: time_delay}.
        """
        super().__init__(sender)
        self.time_delays_table = time_delays_table
