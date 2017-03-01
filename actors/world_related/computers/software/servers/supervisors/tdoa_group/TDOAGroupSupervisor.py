from actor_system.broadcasters.messages.listener_actions import Add as AddListener
from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.software.combination_calculators.tdoa import TDOACombinationCalculator
from actors.world_related.computers.software.combination_calculators.tdoa.messages import CalculateCombinations, \
    CombinationsCalculated
from actors.world_related.computers.software.servers.sensor_groups import TDOASensorGroup
from actors.world_related.computers.software.servers.supervisors.Base import Base
from .messages import FormGroups


class TDOAGroupSupervisor(Base):
    """
    Контроллирует группы звуковых датчиков.
    """

    def __init__(self, computer: Computer):
        """
        Конструктор.
        :param Computer computer: Компьютер, на котором установлена программа.
        """
        super().__init__(computer)
        self.groups = set()
        self._combination_calculator = TDOACombinationCalculator(
            position=None,
            world=None
        )
        self._combination_calculator.groups_formed_broadcaster.tell(
            AddListener(
                sender=self,
                actor=self
            )
        )

    def on_message(self, message: Message):
        if isinstance(message, FormGroups):
            print('on_form_groups started')
            self.on_form_groups(sensor_controllers=message.sensor_controllers)
            print('on_form_groups stopped')
        elif isinstance(message, CombinationsCalculated):
            print('on_combination_calculated started')
            self.on_combinations_calculated(sensor_controllers=message.sensor_controllers,
                                            combinations=message.combinations)
            print('on_combination_calculated stopped')

    def on_form_groups(self, sensor_controllers: list):
        """
        Вызывается каждый раз при необходимости формирования групп из датчиков.
        :param list sensor_controllers: Контроллеры датчиков, из которых нужно сформировать группы.
        :return:
        """
        self._stop_old_groups()
        self._form_combinations(sensor_controllers)

    def on_combinations_calculated(self, sensor_controllers: list, combinations: set):
        self._stop_old_groups()
        self._form_new_groups(sensor_controllers=sensor_controllers, combinations=combinations)
        print('groups formed')

    def _form_combinations(self, sensor_controllers: list):
        self._combination_calculator.tell(
            CalculateCombinations(
                sender=self,
                sensor_controllers=sensor_controllers
            )
        )

    def _form_new_groups(self, sensor_controllers: list, combinations: set):
        """
        Вызывается каждый раз при необходимости формирования групп из датчиков.
        :param list sensor_controllers: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        :return:
        """
        self.groups = {
            TDOASensorGroup(
                computer=self.computer,
                sensor_controllers=combination
            ) for combination in combinations
            }

    def _stop_old_groups(self):
        """
        Остановить работу старых групп датчиков.
        :return:
        """
        for group in self.groups:
            group.stop()
