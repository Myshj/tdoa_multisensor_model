import json

import numpy
import requests
from shapely.geometry import Point

from auxillary.Position import Position


def text_to_json(text: str):
    """
    Конвертирует строку в объект.
    :param text:
    :return:
    """
    return json.loads(text, encoding='utf-8')


def dict_to_point(data: dict):
    """
    Создаёт объект Point из словаря.
    :param data:
    :return:
    """
    return Point(
        data.get('x', 0.0),
        data.get('y', 0.0),
        data.get('z', 0.0)
    )


def get_json_from_server(url: str, credentials: tuple):
    """
    Получает ответ от сервера и конвертирует его в объект.
    :param url:
    :param credentials:
    :return:
    """
    return text_to_json(requests.get(url, auth=credentials).text)


def point_to_array(point: Point):
    """
    Превращает координаты точки в массив.
    :param Point point: Точка с координатами.
    :return numpy.array: numpy.array в формате [x, y, z]
    """
    return numpy.array((point.x, point.y, point.z))


def distance_between_positions(a: Position, b: Position):
    """
    Возвращает расстояние между двумя позициями.
    :param Position a: Точка А.
    :param Position b: Точка В.
    :return float: Расстояние между А и В.
    """
    return numpy.linalg.norm(a.as_array() - b.as_array())
