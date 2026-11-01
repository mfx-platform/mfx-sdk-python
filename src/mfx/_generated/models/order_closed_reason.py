from enum import Enum


class OrderClosedReason(str, Enum):
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    FILLED = "filled"
    REJECTED = "rejected"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
