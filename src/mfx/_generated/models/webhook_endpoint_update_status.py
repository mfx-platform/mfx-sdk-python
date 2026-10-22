from enum import Enum


class WebhookEndpointUpdateStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
