from intervals import IntervalBound, BoundType
from .Base import Base


class IntervalBoundLoader(Base):
    """
    Загружает границы интервалов из базы данных.
    """

    def _restore_actor(self, actor_info: dict):
        """
        Принимает словарь - информацию о границе интервала.
        Возвращает экземпляр класса IntervalBound.
        :param actor_info: {
        'id': int,
        'value': int,
        'bound_type': str;
        }
        :return: IntervalBound
        """
        return IntervalBound(
            value=actor_info['value'],
            bound_type=BoundType.from_string(actor_info['bound_type'])
        )
