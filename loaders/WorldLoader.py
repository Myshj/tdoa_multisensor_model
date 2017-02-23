from actors.worlds import Earth
from .Base import Base


class WorldLoader(Base):
    """
    Загружает сенсоры из базы данных.
    """

    def _restore_actor(self, actor_info: dict):
        """
        Принимает словарь - информацию о мире.
        Возвращает экземпляр Earth.
        :param dict actor_info: Словарь в формате {
        'id': int,
        'name': str,
        'speed_of_sound': float
        }
        :return: SoundSensor.
        """
        return Earth(
            name=actor_info['name'],
            speed_of_sound=actor_info['speed_of_sound']
        )
