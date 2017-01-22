from Actors.WorldRelated.SignalSources import Base as SignalSource
from Signals import Base as Signal
from .Base import Base


class SignalGenerated(Base):
    """
    Сообщение о том, что сигнал сгенерирован.
    """

    def __init__(self, sender, signal: Signal, source: SignalSource):
        """
        Конструктор.
        :param sender: Адресант сообщения.
        :param Signal signal: Информация о сигнале.
        :param SignalSource source: Источник сигнала.
        """
        super().__init__(sender)
        self.signal = signal
        self.source = source
