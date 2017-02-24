from actor_system import Actor
from actor_system.messages import Message
from actors.world_related.computers.software import AbstractSoftware


class AbstractSoftwareEvent(Message):
    """
    Базовый класс для всех сообщениях о событиях, связанных с программным обеспечением.
    """

    def __init__(self, sender: Actor, software: AbstractSoftware):
        super().__init__(sender)
        self.software = software
