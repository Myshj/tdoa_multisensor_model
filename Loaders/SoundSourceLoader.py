import auxillary
from .WorldRelatedObjectLoader import WorldRelatedObjectLoader
from Actors.SignalSources import SoundSource


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
        return SoundSource(
            world=self.worlds[auxillary.get_json_from_server(actor_info['world'], self._credentials)['id']],
            position=auxillary.dict_to_point(auxillary.get_json_from_server(actor_info['position'], self._credentials)),
            interval=actor_info['interval'],
            state=actor_info['state']
        )
