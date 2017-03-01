import itertools

from shapely.geometry import MultiPoint
from shapely.ops import cascaded_union

from actor_system import Broadcaster
from actor_system.broadcasters.messages import Broadcast
from actor_system.messages import Message
from actors.world_related.computers.software.combination_calculators import AbstractCombinationCalculator
from actors.world_related.computers.software.combination_calculators.tdoa.messages import CalculateCombinations, \
    CombinationsCalculated
from actors.worlds import Base as World
from auxillary import Position


class TDOACombinationCalculator(AbstractCombinationCalculator):
    def __init__(self, position: Position, world: World):
        super().__init__(position, world)
        self.groups_formed_broadcaster = Broadcaster()

    def on_message(self, message: Message):
        if isinstance(message, CalculateCombinations):
            self.on_calculate_combinations(message.sensor_controllers)

    def on_calculate_combinations(self, sensor_controllers: list):
        """
        Вызывается каждый раз при необходимости формирования групп датчиков.
        :param list sensor_controllers: Датчики, из которых нужно сформировать группы.
        :return:
        """
        # print('form_groups started')
        self._calculate_combinations(sensor_controllers=sensor_controllers)
        #print('form_groups started')

    def _calculate_combinations(self, sensor_controllers: list):
        """
        Сформировать группы из датчиков.
        НЕ ВСЕГДА ДАЁТ ОПТИМАЛЬНЫЙ РЕЗУЛЬТАТ.
        :param list sensor_controllers: Датчики, из которых нужно сформировать группы.
        :return:
        """

        good_combinations = self._find_all_good_combinations(sensor_controllers)
        combinations_to_return = self._find_combinations_to_return(sensor_controllers, good_combinations)

        self.groups_formed_broadcaster.tell(
            Broadcast(
                sender=self,
                message=CombinationsCalculated(
                    sender=self,
                    sensor_controllers=sensor_controllers,
                    combinations=combinations_to_return
                )
            )
        )

    def _find_combinations_to_return(self, sensor_controllers: list, good_combinations: set):
        """
        Для заданных датчиков находит самые лучшие из возможных комбинаций.
        :param list sensor_controllers: Датчики, из которых нужно сформировать группы.
        :param set good_combinations: Возможные комбинации датчиков.
        :return:
        """
        sensor_to_figure_table = {
            sensor_controller: sensor_controller.sensor.position.as_point() for sensor_controller in sensor_controllers
            }

        forms_from_combinations = {
            combination: MultiPoint(
                [sensor_to_figure_table[sensor_controller] for sensor_controller in combination]
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

    def _find_all_good_combinations(self, sensor_controllers: list):
        """
        Найти все подходящие пятёрки датчиков.
        :param list sensor_controllers: Датчики, из которых нужно сформировать пятёрки.
        :return:
        """
        good_combinations = set()
        for sensor_controller in sensor_controllers:
            # Определили тех, кто может услышать текущего И кого может услышать текущий
            candidates_for_group = {
                candidate for candidate in
                filter(
                    lambda other: other.sensor.radius >= sensor_controller.sensor.position.as_point().distance(
                        other.sensor.position.as_point()) <= sensor_controller.sensor.radius,
                    sensor_controllers
                )
                }

            # Построили УНИКАЛЬНЫЕ пятерки
            for combination in itertools.combinations(candidates_for_group, 5):
                combination = frozenset(
                    candidate for candidate in combination if all(
                        map(
                            lambda other: other.sensor.radius >= candidate.sensor.position.as_point().distance(
                                other.sensor.position.as_point()) <= candidate.sensor.radius,
                            combination
                        )
                    )
                )
                if len(combination) == 5:
                    good_combinations.add(combination)
        return good_combinations
