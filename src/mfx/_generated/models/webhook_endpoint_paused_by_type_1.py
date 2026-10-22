from enum import Enum


class WebhookEndpointPausedByType1(str, Enum):
    OPERATOR = "operator"
    PLATFORM = "platform"
    TENANT = "tenant"

    def __str__(self) -> str:
        return str(self.value)
