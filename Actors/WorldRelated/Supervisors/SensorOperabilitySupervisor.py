import datetime
import gevent
from .Base import Base
from auxillary import Position
from Actors.Worlds import Base as World
from ActorSystem.Messages.ActorActions.ListenerActions import Add as AddListener
from Messages.Reports import SensorState
from Messages.Actions.Supervisors.SensorOperability import ReconfigurationRequired
from Actors.WorldRelated.Sensors import States, Base as Sensor
from ActorSystem import Broadcaster
from ActorSystem.Messages import Broadcast


class SensorOperabilitySupervisor(Base):
    """
    Наблюдатель за работоспособностью датчиков.
    """

    def __init__(self, position: Position, world: World, sensors: list):
        """
        Конструктор.
        :param Position position: Позиция актора в мире.
        :param World world: Мир, к которому прикреплён актор.
        :param list sensors: Датчики, за которыми наблюдает актор.
        """
        super().__init__(position=position, world=world)
        self.reconfiguration_required_broadcaster = Broadcaster()
        self._initialize_tables(sensors)
        self._listen_to_sensors(sensors)

    def on_message(self, message):
        if isinstance(message, SensorState.Alive):
            self.on_sensor_alive(message.sensor)
        elif isinstance(message, SensorState.Broken):
            self.on_sensor_broken(message.sensor)

    def on_sensor_alive(self, sensor: Sensor):
        """
        Вызывается каждый раз при получении сообщения о том, что датчик в порядке.
        :param Sensor sensor: Датчик, о котором идёт речь.
        :return:
        """
        self._update_report_time(sensor)

    def on_sensor_broken(self, sensor: Sensor):
        """
        Вызывается каждый раз при получении сообщения о том, что датчик сломан.
        :param Sensor sensor: Датчик, о котором идёт речь.
        :return:
        """
        self._update_report_time(sensor)
        self._determine_that_sensor_is_broken(sensor)
        self._notify_that_reconfiguration_is_required()

    def on_started(self):
        self._start_supervision_cycle()

    def _initialize_tables(self, sensors: list):
        """
        Инициализация таблиц состояний и времён отчёта датчиков.
        :param list sensors: Датчики, для которых нужно сформировать таблицы.
        :return:
        """
        self._initialize_last_activity_table(sensors)
        self._initialize_state_table(sensors)

    def _initialize_last_activity_table(self, sensors: list):
        """
        Инициализация таблицы последних времён отчёта датчиков.
        :param list sensors: Датчики, для которых формируется таблица.
        :return:
        """
        now = datetime.datetime.now()
        self.last_activity_times = {
            sensor: now for sensor in sensors
            }

    def _initialize_state_table(self, sensors: list):
        """
        Инициализация таблицы состояний датчиков.
        :param list sensors: Датчики, для которых формируется таблица.
        :return:
        """
        self.state_table = {
            sensor: States.Working for sensor in sensors
            }

    def _listen_to_sensors(self, sensors: list):
        """
        Слушать датчики на предмет сообщений о работоспособности.
        :param list sensors: Датчики, которые нужно слушать.
        :return:
        """
        for sensor in sensors:
            self._listen_to_sensor(sensor)

    def _listen_to_sensor(self, sensor: Sensor):
        """
        Слушать датчик на предмет сообщений о работоспособности.
        :param Sensor sensor: Датчик, который нужно слушать.
        :return:
        """
        sensor.alive_broadcaster.tell(AddListener(sender=self, actor=self))

    def _notify_that_reconfiguration_is_required(self):
        """
        Уведомление всех интересующихся о том, что требуется реконфигурация системы.
        :return:
        """
        self.reconfiguration_required_broadcaster.tell(
            Broadcast(
                sender=self,
                message=ReconfigurationRequired(
                    sender=self,
                    sensor_states=self.state_table.copy()
                )
            )
        )

    def _determine_that_sensor_is_broken(self, sensor: Sensor):
        """
        Определить и занести в таблицу факт поломки датчика.
        :param Sensor sensor: Датчик, о котором идёт речь.
        :return:
        """
        self.state_table[sensor] = States.Broken

    def _update_report_time(self, sensor: Sensor):
        """
        Обновить последнее время отчёта для датчика.
        :param Sensor sensor: Датчик, о котором идёт речь.
        :return:
        """
        self.last_activity_times[sensor] = datetime.datetime.now()

    def _start_supervision_cycle(self):
        """
        Старт цикла наблюдения за датчиками.
        :return:
        """
        gevent.spawn(self._supervision_cycle)

    def _supervision_cycle(self):
        """
        Цикл наблюдения за датчиками.
        :return:
        """
        while self._running:
            for sensor in self.last_activity_times.keys():
                if not self._did_sensor_report_recently(sensor):
                    self._determine_that_sensor_is_broken(sensor)
                    self._notify_that_reconfiguration_is_required()

            gevent.sleep()

    def _did_sensor_report_recently(self, sensor: Sensor):
        """
        Рапортовал ли датчик недавно о своей работоспособности?
        :param Sensor sensor: Датчик, о котором идёт речь.
        :return: True, если датчик недавно рапортовал о своей работоспособности. False в ином случае.
        """
        now = datetime.datetime.now()
        return (now - self.last_activity_times[sensor]).total_seconds() <= sensor.heartbeat_interval * 1.2
