from enum import Enum


class RiskActionCompletedKind(str, Enum):
    BLOCK_ENTRIES = "block_entries"
    CANCEL_PENDING = "cancel_pending"
    CLOSE_PART = "close_part"
    CLOSE_POSITIONS = "close_positions"
    MOVE_STOP = "move_stop"
    SET_STOPS = "set_stops"

    def __str__(self) -> str:
        return str(self.value)
