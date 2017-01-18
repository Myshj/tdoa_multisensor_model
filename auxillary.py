import json
import requests
from shapely.geometry import Point


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
        data.get('y', 0.0)
    )


def get_json_from_server(url: str, credentials: tuple):
    """
    Получает ответ от сервера и конвертирует его в объект.
    :param url:
    :param credentials:
    :return:
    """
    return text_to_json(requests.get(url, auth=credentials).text)
