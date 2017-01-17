# -*- coding: utf-8
import Messages
from ActorSystem import Actor
from Actors.ASignalPropagator import ASignalPropagator


class ASignalSource(Actor):
    """
    Источник сигнала.
    При получении команды на выдачу сигнала, выдаёт команду на распространение сигнала связанному распространителю.
    """

    def __init__(self, position, signal_propagator):
        """
        Конструктор.
        :param numpy.array position: Позиция в формате [x, y, z]
        :param ASignalPropagator signal_propagator: Связанный распространитель сигнала.
        """
        super(ASignalSource, self).__init__()
        self.position = position
        self._signal_propagator = signal_propagator

    def on_message(self, message):
        if isinstance(message, Messages.GenerateSignal):
            self._signal_propagator.tell(Messages.Propagate(self, self.position))