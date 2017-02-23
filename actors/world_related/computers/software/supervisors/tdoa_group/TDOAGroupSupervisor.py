from actor_system.broadcasters.messages.listener_actions import Add as AddListener
from actor_system.messages import Message
from actors.world_related.combination_calculators.tdoa import TDOACombinationCalculator
from actors.world_related.combination_calculators.tdoa.messages import CalculateCombinations, CombinationsCalculated
from actors.world_related.computers.software.sensor_groups import TDOASensorGroup
from actors.world_related.computers.software.supervisors.Base import Base
from actors.worlds import Base as World
from auxillary import Position
from .messages import FormGroups


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
        self._combination_calculator = TDOACombinationCalculator(
            position=self.position,
            world=self.world
        )
        self._combination_calculator.groups_formed_broadcaster.tell(
            AddListener(
                sender=self,
                actor=self
            )
        )

    def on_message(self, message: Message):
        if isinstance(message, FormGroups):
            self.on_form_groups(sensors=message.sensors)
        elif isinstance(message, CombinationsCalculated):
            self.on_combinations_calculated(sensors=message.sensors, combinations=message.combinations)

    def on_form_groups(self, sensors: list):
        """
        Вызывается каждый раз при необходимости формирования групп из датчиков.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :return:
        """
        self._stop_old_groups()
        self._form_combinations(sensors)

    def on_combinations_calculated(self, sensors: list, combinations: set):
        self._stop_old_groups()
        self._form_new_groups(sensors=sensors, combinations=combinations)

    def _form_combinations(self, sensors: list):
        self._combination_calculator.tell(
            CalculateCombinations(
                sender=self,
                sensors=sensors
            )
        )

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
