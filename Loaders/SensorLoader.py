import auxillary
from .Base import Base
from Actors.Sensors import SoundSensor


class SensorLoader(Base):
    """
    Загружает сенсоры из базы данных.
    """

    def _restore_actor(self, actor_info: dict):
        """
        Принимает словарь - информацию о сенсоре.
        Возвращает экземпляр SoundSensor.
        :param dict actor_info: Словарь в формате {
        'id': int,
        'position': {
            'x': float,
            'y': float,
            'z': float
        },
        'radius': float,
        'heartbeat_interval': float,
        'state': str
        }
        :return: SoundSensor.
        """
        return SoundSensor(
            auxillary.dict_to_point(auxillary.get_json_from_server(actor_info['position'], self._credentials)),
            actor_info['radius'],
            actor_info['heartbeat_interval'],
            actor_info['state']
        )
