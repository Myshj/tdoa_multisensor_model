from enum import Enum


class States(Enum):
    """
    Состочния датчика.
    """
    Working = 1
    Waiting = 2
    Broken = 3

    @staticmethod
    def from_string(string: str):
        return {
            string == 'working': States.Working,
            string == 'waiting': States.Waiting,
            string == 'broken': States.Broken
        }[True]
