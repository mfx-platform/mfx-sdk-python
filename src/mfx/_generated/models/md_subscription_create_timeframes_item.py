from enum import Enum


class MdSubscriptionCreateTimeframesItem(str, Enum):
    D1 = "D1"
    H1 = "H1"
    H4 = "H4"
    M1 = "M1"
    M15 = "M15"
    M30 = "M30"
    M5 = "M5"
    MN1 = "MN1"
    W1 = "W1"

    def __str__(self) -> str:
        return str(self.value)
