from Messages.Actions.Supervisors.Base import Base as SupervisorMessage
from ActorSystem import Actor


class Base(SupervisorMessage):
    """
    Базовый класс для всех сообщений для наблюдателей за группами TDOA.
    """

    def __init__(self, sender: Actor):
        super().__init__(sender)
