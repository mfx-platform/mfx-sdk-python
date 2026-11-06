from enum import Enum


class RiskAccountRestrictionState(str, Enum):
    ENTRIES_BLOCKED = "entries_blocked"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
