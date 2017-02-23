from actor_system import Actor
from actor_system.messages import Message


class AbstractHardwareEvent(Message):
    """
    Базовый класс для всех сообщений о событиях, связанных с аппаратным обеспечением.
    """

    def __init__(self, sender: Actor, hardware):
        super().__init__(sender)
        self.hardware = hardware
