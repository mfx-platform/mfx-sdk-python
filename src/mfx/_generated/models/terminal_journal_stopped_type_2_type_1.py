from enum import Enum


class TerminalJournalStoppedType2Type1(str, Enum):
    FAILED = "failed"
    RETIRED = "retired"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
