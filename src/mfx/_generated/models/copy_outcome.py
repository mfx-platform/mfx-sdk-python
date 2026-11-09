from enum import Enum


class CopyOutcome(str, Enum):
    FILLED = "filled"
    REFUSED = "refused"
    SKIPPED = "skipped"
    STOPOUT = "stopout"

    def __str__(self) -> str:
        return str(self.value)
