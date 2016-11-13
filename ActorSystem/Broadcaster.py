import ActorSystem.Messages as Messages
from .Actor import Actor


class Broadcaster(Actor):
    def __init__(self):
        super(Broadcaster, self).__init__()
        self._listeners = set()

    def on_message(self, message):
        if isinstance(message, Messages.AddListener):
            self._listeners.add(message.listener)
        elif isinstance(message, Messages.RemoveListener):
            self._listeners.remove(message.listener)
        elif isinstance(message, Messages.Broadcast):
            for listener in self._listeners:
                listener.tell(message.message_to_broadcast)
