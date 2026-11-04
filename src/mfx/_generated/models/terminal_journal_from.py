from enum import Enum


class TerminalJournalFrom(str, Enum):
    LAST_WORDS = "last_words"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
