from enum import Enum


class WebhookAttemptOutcome(str, Enum):
    CONNECTION = "connection"
    REFUSED_ADDRESS = "refused_address"
    STATUS = "status"
    TIMEOUT = "timeout"
    TLS = "tls"

    def __str__(self) -> str:
        return str(self.value)
