from gevent import Greenlet
from gevent.queue import Queue
from ActorSystem.Messages import Message


class Actor(object):
    """
    Базовый класс для всех акторов.
    """

    def __init__(self):
        """
        Конструктор.
        """
        self._inbox = Queue()
        self._running = False
        self.start()

    def start(self):
        """
        Запускает актора.
        :return:
        """
        if not self._running:
            self._running = True
            self.on_started()
            Greenlet.spawn(self._loop)

    def _loop(self):
        while self._running:
            message = self._inbox.get()
            self.on_message(message)

    def stop(self):
        """
        Останавливает актора.
        :return:
        """
        self._running = False
        self.on_stopped()

    def tell(self, message: Message):
        """
        Отослать этому актору сообщение.
        :param message: Сообщение, отсылаемое актору.
        :return:
        """
        if not isinstance(message, Message):
            raise NotImplementedError()
        self._inbox.put(message)

    def on_message(self, message: Message):
        """
        Вызывается каждый раз при получении сообщения.
        :param message:
        :return:
        """
        raise NotImplementedError()

    def on_started(self):
        """
        Вызывается каждый раз при старте актора.
        :return:
        """
        pass

    def on_stopped(self):
        """
        Вызывается каждый раз при остановке актора.
        :return:
        """
        pass
