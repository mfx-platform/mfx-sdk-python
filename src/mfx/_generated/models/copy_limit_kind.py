from enum import Enum


class CopyLimitKind(str, Enum):
    DAILY = "daily"
    LIFETIME = "lifetime"
    MONTHLY = "monthly"

    def __str__(self) -> str:
        return str(self.value)
