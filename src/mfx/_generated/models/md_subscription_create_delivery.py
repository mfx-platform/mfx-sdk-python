from enum import Enum


class MdSubscriptionCreateDelivery(str, Enum):
    REDIS_PUSH = "redis_push"
    WS = "ws"

    def __str__(self) -> str:
        return str(self.value)
