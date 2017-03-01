from actor_system import Actor
from actor_system.broadcasters.messages.listener_actions import Add
from actors.world_related.computers import Computer


class AbstractSoftware(Actor):
    """
    Базовый класс для всего программного обеспечения.
    """

    def __init__(self, computer: Computer):
        """
        Конструктор.
        :param computer: Компьютер, на котором установлено программное обеспечение.
        """
        super().__init__()
        self.computer = computer
        self._start_listening_to_hardware_events()

    def _start_listening_to_hardware_events(self):
        self.computer.hardware_events_broadcaster.tell(
            Add(
                sender=self,
                actor=self
            )
        )
