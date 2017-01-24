from shapely.geometry import Point
import numpy


class Position(object):
    """
    Позиция в пространстве.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Конструктор.
        :param float x: Координата X.
        :param float y: Координата Y.
        :param float z: Координата Z.
        """
        self._point_representation = Point(x, y, z)
        self._array_representation = numpy.array((x, y, z))

    def as_point(self):
        """
        Возвращает позицию в виде точки.
        :return Point: Позиция в виде точки.
        """
        return self._point_representation

    def as_array(self):
        """
        Возвращает позицию в виде массива.
        :return numpy.array: Позиция в виде массива.
        """
        return self._array_representation

    def __str__(self):
        return "Position({0}, {1}, {2})".format(
            self._point_representation.x, self._point_representation.y, self._point_representation.z
        )

    def __repr__(self):
        return "Position({0}, {1}, {2})".format(
            self._point_representation.x, self._point_representation.y, self._point_representation.z
        )
