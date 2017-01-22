from auxillary import functions


class Base(object):
    """
    Базовый класс для всех загрузчиков акторов.
    """

    def __init__(self, url: str, credentials: tuple):
        """
        Конструктор.
        :param str url: Адрес ресурса, с которым работаем.
        :param tuple credentials: Авторизационные данные.
        """
        self._url = url
        self._credentials = credentials

    def load_all(self):
        """
        Загружает акторов из базы данных.
        :return:
        """
        raw_actors = functions.get_json_from_server(self._url, self._credentials)
        return self._restore_actors(raw_actors)

    def _restore_actors(self, raw_data: list):
        """
        Принимает список словарей - информацию об акторах.
        Возвращает словарь в формате {id: Actor,}.
        :param list raw_data: Список словарей.
        :return dict: Словарь в формате {id: Actor}
        """
        return {
            actor_info['id']: self._restore_actor(actor_info) for actor_info in raw_data
            }

    def _restore_actor(self, actor_info: dict):
        """
        Восстанавливает актора из словаря.
        :param dict actor_info:
        :return Actor:
        """
        raise NotImplementedError()
