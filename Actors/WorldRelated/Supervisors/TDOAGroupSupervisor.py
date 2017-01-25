from .Base import Base
from ActorSystem.Messages import Message
from auxillary import Position
from Actors.Worlds import Base as World
from Messages.Actions.Supervisors.TDOA import FormGroups
from Actors.WorldRelated.SensorGroups import TDOASensorGroup


class TDOAGroupSupervisor(Base):
    """
    Контроллирует группы звуковых датчиков.
    """

    def __init__(self, position: Position, world: World):
        """
        Конструктор.
        :param Position position: Позиция актора в мире.
        :param World world: Мир, к которому прикреплён актор.
        """
        super().__init__(position, world)
        self.groups = set()

    def on_message(self, message: Message):
        if isinstance(message, FormGroups):
            self.on_form_groups(sensors=message.sensors, combinations=message.combinations)

    def on_form_groups(self, sensors: list, combinations: set):
        """
        Вызывается каждый раз при необходимости формирования групп из датчиков.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        :return:
        """
        self._stop_old_groups()
        self._form_new_groups(sensors=sensors, combinations=combinations)

    def _form_new_groups(self, sensors: list, combinations: set):
        """
        Вызывается каждый раз при необходимости формирования групп из датчиков.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        :return:
        """
        self.groups = {
            TDOASensorGroup(
                position=Position(0, 0, 0),
                world=self.world,
                sensors=combination
            ) for combination in combinations
            }

    def _stop_old_groups(self):
        """
        Остановить работу старых групп датчиков.
        :return:
        """
        for group in self.groups:
            group.stop()
