from enum import Enum


class PendingOrderOrderType(str, Enum):
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

    def __str__(self) -> str:
        return str(self.value)
