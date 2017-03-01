from actor_system import Actor
from .Base import Base


class FormGroups(Base):
    """
    Сообщение о том, что нужно сформировать группы из датчиков.
    """

    def __init__(self, sender: Actor, sensor_controllers: set):
        """
        Конструктор.
        :param Actor sender: Адресант сообщения.
        :param set sensor_controllers: Контроллеры датчиков, из которых нужно сформировать группы.
        """
        super().__init__(sender)
        self.sensor_controllers = sensor_controllers
