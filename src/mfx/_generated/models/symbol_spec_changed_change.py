from enum import Enum


class SymbolSpecChangedChange(str, Enum):
    REMOVED = "removed"
    SESSIONS = "sessions"
    SPEC = "spec"
    TRADING = "trading"

    def __str__(self) -> str:
        return str(self.value)
