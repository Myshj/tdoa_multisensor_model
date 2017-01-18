import auxillary
from Actors.Sensors import SoundSensor


class SensorLoader(object):
    """
    Загружает сенсоры из базы данных.
    """

    def __init__(self, url: str, credentials: tuple):
        self._url = url
        self._credentials = credentials

    def load_all(self):
        """
        Загружает сенсоры из базы данных.
        Возвращает список готовых к работе сенсоров.
        :return:
        """
        raw_sensors = auxillary.get_json_from_server(self._url, self._credentials)
        return self._restore_actors(raw_sensors)

    def _restore_actors(self, raw_data: list):
        return {
            actor_info['id']: self._restore_actor(actor_info) for actor_info in raw_data
            }

    def _restore_actor(self, actor_info: dict):
        return SoundSensor(
            auxillary.dict_to_point(auxillary.get_json_from_server(actor_info['position'], self._credentials)),
            actor_info['radius'],
            actor_info['heartbeat_interval']
        )
