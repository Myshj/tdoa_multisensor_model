import ActorSystem.Messages.ActorActions.ListenerActions as ListenerActions
from ActorSystem.Messages import Broadcast, Message
from .Actor import Actor


class Broadcaster(Actor):
    """
    Размножает полученные сообщения между многими получателями-слушателями.
    """

    def __init__(self):
        super(Broadcaster, self).__init__()
        self._listeners = set()

    def on_message(self, message: Message):
        if isinstance(message, ListenerActions.Add):
            self._add_listener(message.listener)
        elif isinstance(message, ListenerActions.Remove):
            self._remove_listener(message.listener)
        elif isinstance(message, Broadcast):
            self._broadcast(message.message)

    def _add_listener(self, listener: Actor):
        """
        Добавить актора в список слушателей.
        :param Actor listener: Актор-слушатель.
        :return:
        """
        self._listeners.add(listener)

    def _remove_listener(self, listener: Actor):
        """
        Удалить актора из списка слушателей.
        :param Actor listener: Актор-слушатель.
        :return:
        """
        self._listeners.remove(listener)

    def _broadcast(self, message: Message):
        """
        Размножить сообщение среди слушателей.
        :param Message message: Сообщение для размножения.
        :return:
        """
        for listener in self._listeners:
            listener.tell(message)
