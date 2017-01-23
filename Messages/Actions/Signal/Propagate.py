from .Base import Base
from ActorSystem import Actor
from Signals import Base as Signal
from Actors.WorldRelated.SignalSources import Base as SignalSource


class Propagate(Base):
    """
    Сообщение о том, что нужно распространить сигнал от источника.
    """

    def __init__(self, sender: Actor, signal: Signal, source: SignalSource):
        """

        :param Actor sender: Адресант сообщения.
        :param Signal signal: Информация о сигнале.
        :param SignalSource source: Источник сигнала.
        """
        super().__init__(sender, signal)
        self.source = source
