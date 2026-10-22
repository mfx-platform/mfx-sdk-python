from enum import Enum


class WebhookEndpointResumedBy(str, Enum):
    OPERATOR = "operator"
    TENANT = "tenant"

    def __str__(self) -> str:
        return str(self.value)
