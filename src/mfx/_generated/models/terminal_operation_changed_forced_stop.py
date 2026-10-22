from enum import Enum


class TerminalOperationChangedForcedStop(str, Enum):
    FALSE = "false"
    TRUE = "true"
    VALUE_2 = ""

    def __str__(self) -> str:
        return str(self.value)
