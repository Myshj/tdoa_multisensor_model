from datetime import datetime

from actor_system import Actor
from actor_system.messages import Message
from auxillary import Position


class SensorGroupRecognizedSoundSource(Message):
    """
    Сообщение о том, что группа датчиков распознала источник звука.
    """

    def __init__(
            self,
            sender: Actor,
            when_recognized: datetime,
            estimated_position: Position
    ):
        super().__init__(sender)
        self.when_recognized = when_recognized
        self.estimated_position = estimated_position
