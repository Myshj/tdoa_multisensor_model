from Actors.WorldRelated.SignalSources import SoundSource
from auxillary import functions
from auxillary.Position import Position
from .WorldRelatedObjectLoader import WorldRelatedObjectLoader


class SoundSourceLoader(WorldRelatedObjectLoader):
    """
    Загружает сенсоры из базы данных.
    """

    def _restore_actor(self, actor_info: dict):
        """
        Принимает словарь - информацию об источнике звука.
        Возвращает экземпляр SoundSource.
        :param dict actor_info: Словарь в формате {
        'id': int,
        'position': {
            'x': float,
            'y': float,
            'z': float
        },
        'interval': float,
        'state': str
        }
        :return: SoundSensor.
        """
        p = functions.get_json_from_server(actor_info['position'], self._credentials)
        return SoundSource(
            world=self.worlds[functions.get_json_from_server(actor_info['world'], self._credentials)['id']],
            position=Position(p['x'], p['y'], p['z']),
            interval=actor_info['interval'],
            state=actor_info['state']
        )
