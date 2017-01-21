import auxillary
from .Base import Base
from Actors.SignalSources import SoundSource


class SoundSourceLoader(Base):
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
            auxillary.dict_to_point(auxillary.get_json_from_server(actor_info['position'], self._credentials)),
            actor_info['interval'],
            actor_info['state']
        )
