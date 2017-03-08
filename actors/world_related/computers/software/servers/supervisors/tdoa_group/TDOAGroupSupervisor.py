from actor_system.broadcasters.messages.listener_actions import Add as AddListener
from actor_system.messages import Message
from actors.world_related.computers import Computer
from actors.world_related.computers.software.combination_calculators.tdoa import TDOACombinationCalculator
from actors.world_related.computers.software.combination_calculators.tdoa.messages import CalculateCombinations, \
    CombinationsCalculated
from actors.world_related.computers.software.servers.filters.sound_related.stream_of_position_reports_related.estimated_position_determinators.simple import \
    SimpleEstimatedPositionDeterminator
from actors.world_related.computers.software.servers.sensor_groups import TDOASensorGroup
from actors.world_related.computers.software.servers.supervisors.Base import Base
from actors.world_related.computers.software.servers.supervisors.tdoa_group.messages.position_determinator_operations import *
from actors.world_related.computers.software.servers.sensor_groups.messages.position_determinator_operations import (
    ReportToThisPositionDeterminator as GroupReportToThisPositionDeterminator,
    DoNotReportToThisPositionDeterminator as GroupDoNotReportToThisPositionDeterminator
)
from .messages import FormGroups


class TDOAGroupSupervisor(Base):
    """
    Контроллирует группы звуковых датчиков.
    """

    def __init__(
            self,
            computer: Computer
    ):
        """
        Конструктор.
        :param Computer computer: Компьютер, на котором установлена программа.
        """
        super().__init__(computer)
        self._initialize_position_determinators()
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
        super().on_message(message)
        if isinstance(message, FormGroups):
            # print('on_form_groups started')
            self.on_form_groups(sensor_controllers=message.sensor_controllers)
            # print('on_form_groups stopped')
        elif isinstance(message, CombinationsCalculated):
            # print('on_combination_calculated started')
            self.on_combinations_calculated(sensor_controllers=message.sensor_controllers,
                                            combinations=message.combinations)
            # print('on_combination_calculated stopped')
        elif isinstance(message, AbstractPositionDeterminatorOperation):
            self.on_position_determinator_operation(message)

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
        # print('groups formed')

    def on_position_determinator_operation(self, message: AbstractPositionDeterminatorOperation):
        if isinstance(message, ReportToThisPositionDeterminator):
            self.on_report_to_this_position_determinator(message.position_determinator)
        elif isinstance(message, DoNotReportToThisPositionDeterminator):
            self.on_do_not_report_to_this_position_determinator(message.position_determinator)

    def on_report_to_this_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self._add_related_position_determinator(position_determinator)

    def _add_related_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self.position_determinators.add(position_determinator)

    def _notify_groups_about_added_position_determinator(self,
                                                         position_determinator: SimpleEstimatedPositionDeterminator):
        for group in self.groups:
            group.tell(
                GroupReportToThisPositionDeterminator(
                    sender=self,
                    position_determinator=position_determinator
                )
            )

    def on_do_not_report_to_this_position_determinator(
            self,
            position_determinator: SimpleEstimatedPositionDeterminator
    ):
        self._remove_related_position_determinator(position_determinator)

    def _remove_related_position_determinator(self, position_determinator: SimpleEstimatedPositionDeterminator):
        self.position_determinators.remove(position_determinator)

    def _initialize_position_determinators(self):
        self.position_determinators = set()

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
                sensor_controllers=combination,
                estimated_position_determinators=self.position_determinators.copy()
            ) for combination in combinations
            }

    def _stop_old_groups(self):
        """
        Остановить работу старых групп датчиков.
        :return:
        """
        for group in self.groups:
            group.stop()
