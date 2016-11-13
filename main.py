import json
import gevent

from shapely.geometry import Point

from AModel import AModel

from FillSensors import sensors

if __name__ == '__main__':
    p = Point(10, 10)
    print(p)
    a = sensors
    with open('sensors.json') as sensors_file:
        sensors_raw = json.load(sensors_file)

    with open('sensor_groups.json') as sensor_groups_file:
        sensor_groups_raw = json.load(sensor_groups_file)

    model = AModel(sensors=sensors,
                   sensor_groups=sensor_groups_raw,
                   speed_of_sound=340.29)
    while not model.ended:
        gevent.sleep(1)
