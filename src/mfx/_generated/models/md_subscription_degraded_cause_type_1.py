from enum import Enum


class MdSubscriptionDegradedCauseType1(str, Enum):
    BROKER = "broker"
    PLATFORM = "platform"

    def __str__(self) -> str:
        return str(self.value)
