from actor_system import Actor
from signals import Base as Signal
from actor_system.messages import Message
from actors.world_related.signal_related.sound_related.sources import Base as SignalSource


class PropagateSignal(Message):
    """
    Сообщение о том, что нужно распространить сигнал от источника.
    """

    def __init__(self, sender: Actor, signal: Signal, source: SignalSource):
        """

        :param Actor sender: Адресант сообщения.
        :param Signal signal: Информация о сигнале.
        :param SignalSource source: Источник сигнала.
        """
        super().__init__(sender)
        self.signal = signal
        self.source = source
