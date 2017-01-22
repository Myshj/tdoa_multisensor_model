import itertools

from shapely.geometry import MultiPoint
from shapely.ops import cascaded_union

from ActorSystem import Actor
from ActorSystem.Messages import Message
from Messages import FormGroups


class ASensorGroupFormer(Actor):
    def __init__(self):
        super().__init__()

    def on_message(self, message: Message):
        if isinstance(message, FormGroups):
            self.on_form_groups(message.sender, message.sensors)

    def on_form_groups(self, sender, sensors: list):
        good_combinations = self._find_all_good_combinations(sensors)
        print(good_combinations)

        sensor_to_figure_table = {
            sensor: sensor.position for sensor in sensors
            }

        forms_from_combinations = {
            combination: MultiPoint(
                [sensor_to_figure_table[sensor] for sensor in combination]
            ).convex_hull for combination in good_combinations
            }

        combinations_to_return = good_combinations.copy()

        for current_combination in good_combinations:
            form_with_combination = cascaded_union(
                [forms_from_combinations[combination] for combination in combinations_to_return])
            temp_combinations = good_combinations.copy()
            temp_combinations.remove(current_combination)
            form_without_combination = cascaded_union(
                [forms_from_combinations[combination] for combination in temp_combinations])

            if form_without_combination.almost_equals(form_with_combination):
                combinations_to_return.remove(current_combination)

        print(combinations_to_return)

    def _find_all_good_combinations(self, sensors: list):
        good_combinations = set()
        for sensor in sensors:
            # Определили тех, кто может услышать текущего И кого может услышать текущий
            candidates_for_group = {
                candidate for candidate in filter(
                lambda other: other.radius >=
                              sensor.position.distance(other.position) <=
                              sensor.radius and other, sensors)
                }

            # Построили УНИКАЛЬНЫЕ пятерки
            for combination in itertools.combinations(candidates_for_group, 5):
                combination = frozenset(
                    candidate for candidate in combination if all(
                        map(
                            lambda other: other.radius >= candidate.position.distance(
                                other.position) <= candidate.radius,
                            combination
                        )
                    )
                )
                if len(combination) == 5:
                    good_combinations.add(combination)
        return good_combinations
