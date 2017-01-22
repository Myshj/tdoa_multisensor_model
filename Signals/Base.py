from datetime import datetime


class Base(object):
    """
    Базовый класс для всех сигналов.
    """

    def __init__(self, when_generated: datetime):
        """
        Конструктор.
        :param datetime when_generated: Когда сигнал был сгенерирован.
        """
        self.when_generated = when_generated
