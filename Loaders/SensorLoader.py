import auxillary
from .WorldRelatedObjectLoader import WorldRelatedObjectLoader
from Actors.Sensors import SoundSensor


class SensorLoader(WorldRelatedObjectLoader):
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
            world=self.worlds[auxillary.get_json_from_server(actor_info['world'], self._credentials)['id']],
            position=auxillary.dict_to_point(auxillary.get_json_from_server(actor_info['position'], self._credentials)),
            radius=actor_info['radius'],
            heartbeat_interval=actor_info['heartbeat_interval'],
            state=actor_info['state']
        )
