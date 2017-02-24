from actor_system import Actor
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
