from enum import Enum


class CopyLogEntryAction(str, Enum):
    CLOSE = "close"
    CLOSE_PART = "close_part"
    MODIFY = "modify"
    OPEN = "open"
    PENDING_CANCEL = "pending_cancel"
    PENDING_MODIFY = "pending_modify"
    PENDING_PLACE = "pending_place"

    def __str__(self) -> str:
        return str(self.value)
