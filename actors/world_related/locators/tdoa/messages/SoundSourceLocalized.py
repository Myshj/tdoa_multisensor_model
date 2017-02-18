from .Base import Base
from actor_system import Actor
from auxillary import Position


class SoundSourceLocalized(Base):
    """
    Сообщение о том, что обнаружен источник звука на ожидаемой позиции.
    """

    def __init__(self, sender: Actor, estimated_position: Position):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param Position estimated_position: Ожидаемая позиция источника звука.
        """
        super().__init__(sender)
        self.estimated_position = estimated_position
