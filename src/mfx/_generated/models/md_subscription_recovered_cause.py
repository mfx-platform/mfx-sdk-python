from enum import Enum


class MdSubscriptionRecoveredCause(str, Enum):
    BROKER = "broker"
    PLATFORM = "platform"

    def __str__(self) -> str:
        return str(self.value)
