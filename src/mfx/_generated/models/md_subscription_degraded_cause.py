from enum import Enum


class MdSubscriptionDegradedCause(str, Enum):
    BROKER = "broker"
    PLATFORM = "platform"

    def __str__(self) -> str:
        return str(self.value)
