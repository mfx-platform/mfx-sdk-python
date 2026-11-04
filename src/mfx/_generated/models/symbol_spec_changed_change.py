from enum import Enum


class SymbolSpecChangedChange(str, Enum):
    ADDED = "added"
    CAME_BACK = "came_back"
    DESCRIPTION = "description"
    IDENTITY = "identity"
    REMOVED = "removed"
    SESSIONS = "sessions"
    SPEC = "spec"
    TRADING = "trading"

    def __str__(self) -> str:
        return str(self.value)
