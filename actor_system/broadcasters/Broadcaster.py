from actor_system.Actor import Actor
from actor_system.messages import Message
from .messages import listener_actions, Broadcast


class Broadcaster(Actor):
    """
    Размножает полученные сообщения между многими получателями-слушателями.
    """

    def __init__(self):
        super(Broadcaster, self).__init__()
        self._listeners = set()

    def on_message(self, message: Message):
        if isinstance(message, listener_actions.Add):
            self._add_listener(message.actor)
        elif isinstance(message, listener_actions.Remove):
            self._remove_listener(message.actor)
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
