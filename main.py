import settings
import Loaders
import gevent
from ActorSystem.Messages import Message

if __name__ == '__main__':
    world_loader = Loaders.WorldLoader(
        url=settings.worlds_url,
        credentials=settings.credentials
    )
    worlds = world_loader.load_all()

    sensor_loader = Loaders.SensorLoader(
        url=settings.sensors_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sensors = sensor_loader.load_all()

    sound_source_loader = Loaders.SoundSourceLoader(
        url=settings.sound_sources_url,
        credentials=settings.credentials,
        worlds=worlds
    )
    sound_sources = sound_source_loader.load_all()
    print(sound_sources)
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    sensors[2].tell(Message(None))
    while True:
        gevent.sleep(1)
