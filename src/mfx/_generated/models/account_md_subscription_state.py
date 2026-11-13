from enum import Enum


class AccountMdSubscriptionState(str, Enum):
    PENDING = "pending"
    STOPPED = "stopped"
    STREAMING = "streaming"

    def __str__(self) -> str:
        return str(self.value)
