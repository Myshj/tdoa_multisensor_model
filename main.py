import settings
import Loaders
import gevent
from ActorSystem.Messages import Message

if __name__ == '__main__':
    sensor_loader = Loaders.SensorLoader(settings.sensors_url, settings.credentials)
    sensors = sensor_loader.load_all()

    sound_source_loader = Loaders.SoundSourceLoader(settings.sound_sources_url, settings.credentials)
    sound_sources = sound_source_loader.load_all()
    print(sound_sources)
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    while True:
        gevent.sleep(1)
