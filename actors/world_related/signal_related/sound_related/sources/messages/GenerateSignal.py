from .Base import Base


class GenerateSignal(Base):
    """
    Запрос к источнику сигнала на генерацию сигнала.
    """
    def __init__(self, sender):
        super().__init__(sender)
