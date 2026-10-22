from enum import Enum


class MdSubscriptionState(str, Enum):
    DEGRADED = "degraded"
    PENDING = "pending"
    STOPPED = "stopped"
    STREAMING = "streaming"

    def __str__(self) -> str:
        return str(self.value)
