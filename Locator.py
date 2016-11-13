# -*- coding: utf-8
import numpy


class Locator(object):
    """
    Вычисляет позицию источника звука на основании скорости звука и задержек между прибытиями сигнала на датчики.
    """

    def __init__(self, microphone_positions, speed_of_sound=340.29):
        self._speed_of_sound = speed_of_sound
        self._inverted_speed_of_sound = 1 / self._speed_of_sound
        self._count_of_microphones = len(microphone_positions)
        self._initialize_microphone_positions(microphone_positions)
        self._initialize_squared_microphone_positions()

        self._initialize_sums_for_abc()

    def locate(self, transit_times):
        self._initialize_transit_times(transit_times)
        self._initialize_differences_in_transit_times()

        self._initialize_column_a()
        self._initialize_column_b()
        self._initialize_column_c()
        self._initialize_column_d()

        self._left_matrix = numpy.column_stack((self._column_a, self._column_b, self._column_c))

        new_m = numpy.linalg.pinv(self._left_matrix)
        self._result = numpy.dot(new_m, self._column_d)

        return self._result

    def _initialize_microphone_positions(self, microphone_positions):
        self._microphone_positions = numpy.matrix([
                                                      microphone_position for
                                                      microphone_position in microphone_positions
                                                      ])

    def _initialize_transit_times(self, transit_times):
        self._transit_times_between_microphones_and_source = numpy.array(transit_times)

    def _initialize_differences_in_transit_times(self):
        self._differences_in_transit_times = numpy.array([
                                                             transit_time -
                                                             self._transit_times_between_microphones_and_source[0] for
                                                             transit_time in
                                                             self._transit_times_between_microphones_and_source
                                                             ])

    def _initialize_squared_microphone_positions(self):
        squared_microphone_positions = numpy.square(self._microphone_positions)
        self._sums_for_d = numpy.array([
                                           numpy.sum(squared_microphone_positions[i]) for i in
                                           range(0, self._count_of_microphones)
                                           ])

    def _initialize_sums_for_abc(self):
        self._sums_for_abc = 2 * self._microphone_positions - 2 * self._microphone_positions[0]

    def _initialize_column_a(self):
        self._column_a = numpy.zeros(self._count_of_microphones - 2)
        for i in range(2, self._count_of_microphones):
            self._column_a[i - 2] = self._calculate_element_for_column_a(i)

    def _calculate_element_for_column_a(self, i):
        return self._inverted_speed_of_sound / self._differences_in_transit_times[i] * self._sums_for_abc[i, 0] - \
               self._inverted_speed_of_sound / self._differences_in_transit_times[1] * self._sums_for_abc[1, 0]

    def _initialize_column_b(self):
        self._column_b = numpy.zeros(self._count_of_microphones - 2)
        for i in range(2, self._count_of_microphones):
            self._column_b[i - 2] = self._calculate_element_for_column_b(i)

    def _calculate_element_for_column_b(self, i):
        return self._inverted_speed_of_sound / self._differences_in_transit_times[i] * self._sums_for_abc[i, 1] - \
               self._inverted_speed_of_sound / self._differences_in_transit_times[1] * self._sums_for_abc[1, 1]

    def _initialize_column_c(self):
        self._column_c = numpy.zeros(self._count_of_microphones - 2)
        for i in range(2, self._count_of_microphones):
            self._column_c[i - 2] = self._calculate_element_for_column_c(i)

    def _calculate_element_for_column_c(self, i):
        return self._inverted_speed_of_sound / self._differences_in_transit_times[i] * self._sums_for_abc[i, 2] - \
               self._inverted_speed_of_sound / self._differences_in_transit_times[1] * self._sums_for_abc[1, 2]

    def _initialize_column_d(self):
        self._column_d = numpy.zeros(self._count_of_microphones - 2)
        for i in range(2, self._count_of_microphones):
            self._column_d[i - 2] = self._calculate_element_for_column_d(i)

    def _calculate_element_for_column_d(self, i):
        return -(
            self._speed_of_sound * (self._differences_in_transit_times[i] - self._differences_in_transit_times[1]) +
            self._inverted_speed_of_sound / self._differences_in_transit_times[i] * (
                self._sums_for_d[0] - self._sums_for_d[i]) - self._inverted_speed_of_sound /
            self._differences_in_transit_times[1] * (self._sums_for_d[0] - self._sums_for_d[1])
        )
