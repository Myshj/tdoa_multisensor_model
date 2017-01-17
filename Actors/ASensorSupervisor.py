import datetime
import gevent
import Messages
import ActorSystem.Messages
from ActorSystem import Actor


class ASensorSupervisor(Actor):
    def __init__(self, sensors):
        super(ASensorSupervisor, self).__init__()
        now = datetime.datetime.now()
        self.activity_table = {
            sensor: now for sensor in sensors
            }
        self.state_table = {
            sensor: 'ok' for sensor in sensors
            }
        for sensor in sensors:
            sensor.alive_broadcaster.tell(ActorSystem.Messages.AddListener(self, listener=self))

    def on_message(self, message):
        if isinstance(message, Messages.Alive):
            if message.who in self.activity_table.keys():
                self.activity_table[message.who] = datetime.datetime.now()

    def on_started(self):
        self._start_supervision()

    def _start_supervision(self):
        gevent.spawn(self._supervision_cycle)

    def _supervision_cycle(self):
        while self._running:
            now = datetime.datetime.now()
            for sensor in self.activity_table.keys():
                if (now - self.activity_table[sensor]).total_seconds() > sensor.heartbeat_interval * 1.2:
                    self.state_table[sensor] = 'bad'

            gevent.sleep()
