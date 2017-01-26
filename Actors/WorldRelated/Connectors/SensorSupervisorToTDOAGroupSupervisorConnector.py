from .Base import Base
from auxillary import Position
from Actors.Worlds import Base as World
from Actors.WorldRelated.Supervisors import SensorOperabilitySupervisor, TDOAGroupSupervisor
from ActorSystem.Messages import Broadcast, Message
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from Messages.Actions.Supervisors.SensorOperability import ReconfigurationRequired
from Actors.WorldRelated.Sensors import States
from Messages.Actions.Supervisors.TDOA import FormGroups


class SensorSupervisorToTDOAGroupSupervisorConnector(Base):
    """
    Уведомляет наблюдателя за группами датчиков о необходимости переконфигурирования системы.
    """

    def __init__(
            self,
            position: Position,
            world: World,
            sensor_operability_supervisor: SensorOperabilitySupervisor,
            tdoa_group_supervisor: TDOAGroupSupervisor
    ):
        """
        Конструктор.
        :param Position position: Позиция актора в мире.
        :param World world: Мир, к которому прикреплён актор.
        :param SensorOperabilitySupervisor sensor_operability_supervisor: Связанный наблюдатель за работоспособностью датчиков.
        :param TDOAGroupSupervisor tdoa_group_supervisor: Связанный наблюдатель за группами датчиков.
        """
        super().__init__(position, world)
        self.sensor_operability_supervisor = sensor_operability_supervisor
        self._listen_to_sensor_operability_supervisor(sensor_operability_supervisor)
        self.tdoa_group_supervisor = tdoa_group_supervisor

    def on_message(self, message: Message):
        if isinstance(message, ReconfigurationRequired):
            self.on_reconfiguration_required(message.sensor_states)

    def on_reconfiguration_required(self, sensor_states: dict):
        """
        Вызывается каждый раз при необходимости переконфигурирования системы.
        :param sensor_states: Словарь в формате: {sensor: state}
        :return:
        """
        self._notify_tdoa_group_supervisor(sensors=self._find_working_sensors(sensor_states))

    def _notify_tdoa_group_supervisor(self, sensors: set):
        """
        Уведомить наблюдателя за группами датчиков о неободимости переконфигурирования системы.
        :param set sensors: Датчики, из которых нужно сформировать группы.
        :return:
        """
        self.tdoa_group_supervisor.tell(
            FormGroups(
                sender=self,
                sensors=sensors
            )
        )

    def _find_working_sensors(self, sensor_states: dict):
        """
        Выбрать из таблицы работоспособные датчики.
        :param sensor_states: Словарь в формате: {sensor: state}
        :return:
        """
        ret = set()
        for sensor, state in sensor_states:
            if state == States.Working:
                ret.add(sensor)
        return ret

    def _listen_to_sensor_operability_supervisor(self, sensor_operability_supervisor: SensorOperabilitySupervisor):
        """
        Слушать наблюдателя за работоспособностью датчиков на предмет сообщений об изменении конфигурации системы.
        :param SensorOperabilitySupervisor sensor_operability_supervisor: Связанный наблюдатель за работоспособностью датчиков.
        :return:
        """
        sensor_operability_supervisor.reconfiguration_required_broadcaster.tell(
            Broadcast(
                sender=self,
                message=AddListener(
                    sender=self,
                    actor=self
                )
            )
        )
