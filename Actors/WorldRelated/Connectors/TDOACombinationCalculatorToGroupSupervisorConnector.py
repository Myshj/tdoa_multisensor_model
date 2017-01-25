from .Base import Base
from auxillary import Position
from Actors.Worlds import Base as World
from Actors.WorldRelated.CombinationCalculators import TDOACombinationCalculator
from Actors.WorldRelated.Supervisors import TDOAGroupSupervisor
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from ActorSystem.Messages import Message
from Messages.Actions.CombinationCalculator import CombinationsCalculated
from Messages.Actions.Supervisors.TDOA import FormGroups


class TDOACombinationCalculatorToGroupSupervisorConnector(Base):
    """
    Уведомляет наблюдателя за группами о необходимости формирования групп.
    """

    def __init__(
            self,
            position: Position,
            world: World,
            combination_calculator: TDOACombinationCalculator,
            group_supervisor: TDOAGroupSupervisor
    ):
        """
        Конструктор.
        :param Position position: Позиция актора в мире.
        :param World world: Мир, к которому прикреплён актор.
        :param TDOACombinationCalculator combination_calculator: Связанный вычислитель комбинаций датчиков.
        :param TDOAGroupSupervisor group_supervisor: Связанный наблюдатель за группами датчиков.
        """
        super().__init__(position, world)
        self.combination_calculator = combination_calculator
        self._listen_to_combination_calculator(combination_calculator)
        self.group_supervisor = group_supervisor

    def on_message(self, message: Message):
        if isinstance(message, CombinationsCalculated):
            self.on_combinations_calculated(sensors=message.sensors, combinations=message.combinations)

    def on_combinations_calculated(self, sensors: list, combinations: set):
        """
        Вызывается каждый раз при получении уведомления о формировании комбинаций датчиков.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        :return:
        """
        self._notify_group_supervisor(sensors=sensors, combinations=combinations)

    def _notify_group_supervisor(self, sensors: list, combinations: set):
        """
        Уведомить наблюдателя за группами о необходимости формирования новых групп.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set combinations: Подходящие для групп комбинации датчиков.
        :return:
        """
        self.group_supervisor.tell(
            FormGroups(
                sender=self,
                sensors=sensors,
                combinations=combinations
            )
        )

    def _listen_to_combination_calculator(self, combination_calculator: TDOACombinationCalculator):
        """
        Слушать вычислителя комбинаций на предмет сообщений о формировании комбинаций датчиков.
        :param TDOACombinationCalculator combination_calculator: Вычислитель комбинаций, слушать которого нужно.
        :return:
        """
        combination_calculator.groups_formed_broadcaster.tell(
            AddListener(
                sender=self,
                actor=self
            )
        )
