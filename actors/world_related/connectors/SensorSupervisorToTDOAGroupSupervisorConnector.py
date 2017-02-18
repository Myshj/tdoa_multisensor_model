from actor_system.broadcasters.messages.listener_actions import Add as AddListener
from actor_system.messages import Message
from actors.world_related.signal_related.sound_related.sensors import States
from actors.world_related.supervisors import SensorOperabilitySupervisor, TDOAGroupSupervisor
from actors.world_related.supervisors.sensor_operability.messages import ReconfigurationRequired
from actors.world_related.supervisors.tdoa_group.messages import FormGroups
from actors.worlds import Base as World
from auxillary import Position
from .Base import Base


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
        for sensor in sensor_states.keys():
            if sensor_states[sensor] == States.Working:
                ret.add(sensor)
        return ret

    def _listen_to_sensor_operability_supervisor(self, sensor_operability_supervisor: SensorOperabilitySupervisor):
        """
        Слушать наблюдателя за работоспособностью датчиков на предмет сообщений об изменении конфигурации системы.
        :param SensorOperabilitySupervisor sensor_operability_supervisor: Связанный наблюдатель за работоспособностью датчиков.
        :return:
        """
        sensor_operability_supervisor.reconfiguration_required_broadcaster.tell(
            message=AddListener(
                sender=self,
                actor=self
            )
        )
