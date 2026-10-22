from enum import Enum


class TerminalConditionChangedAttributedTo(str, Enum):
    BROKER = "broker"
    VALUE_1 = ""

    def __str__(self) -> str:
        return str(self.value)
