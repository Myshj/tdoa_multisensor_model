from .AbstractLoader import AbstractLoader


class WorldRelatedObjectLoader(AbstractLoader):
    """
    Загружает связанные с мирами объекты.
    """

    def __init__(self, url: str, credentials: tuple, worlds: dict):
        """
        Конструктор.
        :param str url: Адрес ресурса, с которым работаем.
        :param tuple credentials: Авторизационные данные.
        :param dict worlds: Словарь миров в формате {id: actors.worlds.Earth}
        """
        super().__init__(url, credentials)
        self.worlds = worlds
