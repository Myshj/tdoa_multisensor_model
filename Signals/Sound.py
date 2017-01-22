from .Base import Base
from datetime import datetime


class Sound(Base):
    """
    Звуковой сигнал.
    """

    def __init__(self, when_generated: datetime):
        """
        Конструктор.
        :param datetime when_generated: Когда сигнал был сгенерирован.
        """
        super().__init__(when_generated)
