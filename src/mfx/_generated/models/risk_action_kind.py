from enum import Enum


class RiskActionKind(str, Enum):
    BLOCK_ENTRIES = "block_entries"
    CANCEL_PENDING = "cancel_pending"
    CLOSE_POSITIONS = "close_positions"
    NOTIFY = "notify"

    def __str__(self) -> str:
        return str(self.value)
