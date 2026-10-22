from enum import Enum


class ConditionStatus(str, Enum):
    FAILED = "failed"
    OK = "ok"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
