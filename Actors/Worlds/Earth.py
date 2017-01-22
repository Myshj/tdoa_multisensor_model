from .Base import Base


class Earth(Base):
    """
    Землеподобный мир.
    """

    def __init__(self, name: str, speed_of_sound: float):
        """
        Конструктор.
        :param str name: Название мира.
        :param float speed_of_sound: Скорость звука в метрах в секунду.
        """
        super().__init__(name)
        self.speed_of_sound = speed_of_sound
