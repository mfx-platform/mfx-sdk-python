from enum import Enum


class ListWebhookFailuresStateItem(str, Enum):
    DEAD = "dead"
    DELIVERED = "delivered"
    RETRYING = "retrying"

    def __str__(self) -> str:
        return str(self.value)
