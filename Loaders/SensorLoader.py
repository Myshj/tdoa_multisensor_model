from actors.world_related.signal_related.sound_related.sensors import SoundSensor, States
from auxillary import functions
from auxillary.Position import Position
from .WorldRelatedObjectLoader import WorldRelatedObjectLoader


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
        p = functions.get_json_from_server(actor_info['position'], self._credentials)
        return SoundSensor(
            world=self.worlds[functions.get_json_from_server(actor_info['world'], self._credentials)['id']],
            position=Position(p['x'], p['y'], p['z']),
            radius=actor_info['radius'],
            heartbeat_interval=actor_info['heartbeat_interval'],
            failure_probability=actor_info['failure_probability'],
            state=States.from_string(actor_info['state'])
        )
