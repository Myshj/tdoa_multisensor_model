import itertools

from shapely.geometry import MultiPoint
from shapely.ops import cascaded_union

from ActorSystem import Broadcaster
from ActorSystem.Messages import Message, Broadcast
from actors.world_related.combination_calculators.Base import Base
from actors.world_related.combination_calculators.tdoa.messages import CalculateCombinations, CombinationsCalculated
from actors.worlds import Base as World
from auxillary import Position


class TDOACombinationCalculator(Base):
    def __init__(self, position: Position, world: World):
        super().__init__(position, world)
        self.groups_formed_broadcaster = Broadcaster()

    def on_message(self, message: Message):
        if isinstance(message, CalculateCombinations):
            self.on_form_groups(message.sensors)

    def on_form_groups(self, sensors: list):
        """
        Вызывается каждый раз при необходимости формирования групп датчиков.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :return:
        """
        self._form_groups(sensors=sensors)

    def _form_groups(self, sensors: list):
        """
        Сформировать группы из датчиков.
        НЕ ВСЕГДА ДАЁТ ОПТИМАЛЬНЫЙ РЕЗУЛЬТАТ.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :return:
        """
        good_combinations = self._find_all_good_combinations(sensors)
        combinations_to_return = self._find_combinations_to_return(sensors, good_combinations)

        self.groups_formed_broadcaster.tell(
            Broadcast(
                sender=self,
                message=CombinationsCalculated(
                    sender=self,
                    sensors=sensors,
                    combinations=combinations_to_return
                )
            )
        )

    def _find_combinations_to_return(self, sensors: list, good_combinations: set):
        """
        Для заданных датчиков находит самые лучшие из возможных комбинаций.
        :param list sensors: Датчики, из которых нужно сформировать группы.
        :param set good_combinations: Возможные комбинации датчиков.
        :return:
        """
        sensor_to_figure_table = {
            sensor: sensor.position.as_point() for sensor in sensors
            }

        forms_from_combinations = {
            combination: MultiPoint(
                [sensor_to_figure_table[sensor] for sensor in combination]
            ).convex_hull for combination in good_combinations
            }

        combinations_to_return = good_combinations.copy()

        for current_combination in good_combinations:
            form_with_combination = cascaded_union(
                [forms_from_combinations[combination] for combination in combinations_to_return]
            )
            temp_combinations = good_combinations.copy()
            temp_combinations.remove(current_combination)
            form_without_combination = cascaded_union(
                [forms_from_combinations[combination] for combination in temp_combinations]
            )

            if form_without_combination.almost_equals(form_with_combination):
                combinations_to_return.remove(current_combination)

        return combinations_to_return

    def _find_all_good_combinations(self, sensors: list):
        """
        Найти все подходящие пятёрки датчиков.
        :param list sensors: Датчики, из которых нужно сформировать пятёрки.
        :return:
        """
        good_combinations = set()
        for sensor in sensors:
            # Определили тех, кто может услышать текущего И кого может услышать текущий
            candidates_for_group = {
                candidate for candidate in
                filter(
                    lambda other: other.radius >= sensor.position.as_point().distance(
                        other.position.as_point()) <= sensor.radius,
                    sensors
                )
                }

            # Построили УНИКАЛЬНЫЕ пятерки
            for combination in itertools.combinations(candidates_for_group, 5):
                combination = frozenset(
                    candidate for candidate in combination if all(
                        map(
                            lambda other: other.radius >= candidate.position.as_point().distance(
                                other.position.as_point()) <= candidate.radius,
                            combination
                        )
                    )
                )
                if len(combination) == 5:
                    good_combinations.add(combination)
        return good_combinations
