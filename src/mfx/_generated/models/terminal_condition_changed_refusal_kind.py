from enum import Enum


class TerminalConditionChangedRefusalKind(str, Enum):
    INVALID_ACCOUNT = "invalid_account"
    OTHER = "other"
    VALUE_2 = ""

    def __str__(self) -> str:
        return str(self.value)
