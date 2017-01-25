from .Base import Base
from auxillary import Position
from ActorSystem.Messages import Message
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from Actors.Worlds import Base as World
from Actors.WorldRelated.SignalSources import SoundSource
from Actors.WorldRelated.SignalPropagators import SoundPropagator
from Signals import Sound
from Messages.Actions.SignalSource import SignalGenerated
from Messages.Actions.Signal import Propagate


class SoundSourceToPropagatorConnector(Base):
    """
    Уведомляет распространителя сигнала о факте генерации сигнала.
    """

    def __init__(self, position: Position, world: World, source: SoundSource, propagator: SoundPropagator):
        """
        Конструктор.
        :param Position position: Позиция в мире.
        :param World world: Мир, в котором существует соединитель.
        :param SoundSource source: Связанный источник сигнала.
        :param SoundPropagator propagator: Связанный распространитель сигнала.
        """
        super().__init__(position=position, world=world)
        self.source = source
        self._listen_to_source(source)
        self.propagator = propagator

    def on_message(self, message: Message):
        if isinstance(message, SignalGenerated):
            self.on_signal_generated(signal=message.signal, source=message.source)

    def _listen_to_source(self, source: SoundSource):
        """
        Слушать источник звука на предмет генерации сигналов.
        :param SoundSource source: Источник, который нужно слушать.
        :return:
        """
        source.signal_generated_broadcaster.tell(
            AddListener(
                sender=self,
                actor=self
            )
        )

    def on_signal_generated(self, signal: Sound, source: SoundSource):
        """
        Вызывается каждый раз, когда связанный источник звука генерирует сигнал.
        :param Sound signal: Сгенерированный сигнал.
        :param SoundSource source: Источник, выдавший сигнал.
        :return:
        """
        self._notify_propagator(signal=signal, source=source)

    def _notify_propagator(self, signal: Sound, source: SoundSource):
        """
        Уведомить связанного распространителя сигнала о необходимости распространения сгенерированного сигнала.
        :param Sound signal: Сгенерированный сигнал.
        :param SoundSource source: Источник, выдавший сигнал.
        :return:
        """
        self.propagator.tell(
            Propagate(
                sender=self,
                signal=signal,
                source=source
            )
        )
