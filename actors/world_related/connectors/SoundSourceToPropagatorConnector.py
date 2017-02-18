from ActorSystem.Messages import Message
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from Signals import Sound
from actors.world_related.signal_related.sound_related.propagators import SoundPropagator
from actors.world_related.signal_related.sound_related.propagators.messages import PropagateSignal
from actors.world_related.signal_related.sound_related.sources import SoundSource
from actors.world_related.signal_related.sound_related.sources.messages import SignalGenerated
from actors.worlds import Base as World
from auxillary import Position
from .Base import Base


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
            PropagateSignal(
                sender=self,
                signal=signal,
                source=source
            )
        )
