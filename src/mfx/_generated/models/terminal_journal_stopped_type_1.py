from enum import Enum


class TerminalJournalStoppedType1(str, Enum):
    FAILED = "failed"
    RETIRED = "retired"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
