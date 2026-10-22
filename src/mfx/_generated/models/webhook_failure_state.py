from enum import Enum


class WebhookFailureState(str, Enum):
    DEAD = "dead"
    DELIVERED = "delivered"
    RETRYING = "retrying"

    def __str__(self) -> str:
        return str(self.value)
