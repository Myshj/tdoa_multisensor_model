from .AbstractLoader import AbstractLoader
from intervals import Interval
from auxillary import functions


class IntervalLoader(AbstractLoader):
    """
    Загружает интервалы.
    """

    def __init__(self, url: str, credentials: tuple, interval_bounds: dict):
        super().__init__(url, credentials)
        self.interval_bounds = interval_bounds

    def _restore_actor(self, actor_info: dict):
        """

        :param actor_info: {
        'id': int,
        'lower_bound': str,
        'upper_bound': str
        }
        :return:
        """
        lower_bound_dict = functions.get_json_from_server(actor_info['lower_bound'], credentials=self._credentials)
        upper_bound_dict = functions.get_json_from_server(actor_info['upper_bound'], credentials=self._credentials)

        return Interval(
            left_bound=self.interval_bounds[lower_bound_dict['id']],
            right_bound=self.interval_bounds[upper_bound_dict['id']]
        )
