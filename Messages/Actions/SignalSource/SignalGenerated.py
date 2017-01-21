from datetime import datetime
from .Base import Base
from Actors.SignalSources import Base as SignalSource


class SignalGenerated(Base):
    """
    Сообщение о том, что сигнал сгенерирован.
    """

    def __init__(self, sender, signal, source: SignalSource, when: datetime):
        """
        Конструктор.
        :param sender: Адресант сообщения.
        :param signal: Информация о сигнале.
        :param SignalSource source: Источник сигнала.
        :param datetime when: Когда сигнал был сгенерирован.
        """
        super().__init__(sender)
        self.signal = signal
        self.source = source
        self.when = when
