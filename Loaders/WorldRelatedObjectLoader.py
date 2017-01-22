from .Base import Base


class WorldRelatedObjectLoader(Base):
    """
    Загружает связанные с мирами объекты.
    """

    def __init__(self, url: str, credentials: tuple, worlds: dict):
        """
        Конструктор.
        :param str url: Адрес ресурса, с которым работаем.
        :param tuple credentials: Авторизационные данные.
        :param dict worlds: Словарь миров в формате {id: Actors.Worlds.Earth}
        """
        super().__init__(url, credentials)
        self.worlds = worlds
