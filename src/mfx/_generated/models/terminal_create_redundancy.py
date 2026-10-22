from enum import Enum


class TerminalCreateRedundancy(str, Enum):
    ACTIVE_ACTIVE = "active_active"
    ACTIVE_PASSIVE = "active_passive"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
