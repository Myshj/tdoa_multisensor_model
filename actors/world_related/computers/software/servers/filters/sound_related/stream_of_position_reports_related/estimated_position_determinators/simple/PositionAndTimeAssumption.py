from datetime import datetime

from auxillary import Position


class PositionAndTimeAssumption(object):
    """
    Предположение о позиции источника звука в момент времени.
    """

    def __init__(
            self,
            position: Position,
            time: datetime
    ):
        super().__init__()
        self.position = position
        self.time = time
