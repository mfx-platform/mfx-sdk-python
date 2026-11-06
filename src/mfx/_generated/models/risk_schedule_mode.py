from enum import Enum


class RiskScheduleMode(str, Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"

    def __str__(self) -> str:
        return str(self.value)
