from enum import Enum


class CopySignalEntryAction(str, Enum):
    CLOSE = "close"
    CLOSE_PART = "close_part"
    MODIFY = "modify"
    OPEN = "open"
    PENDING_CANCEL = "pending_cancel"
    PENDING_MODIFY = "pending_modify"
    PENDING_PLACE = "pending_place"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CopySignalEntryAction":
        """A word from a response: its member, or, for a word a later version of the API added,
        an UNKNOWN pseudo-member whose value is the word as sent."""
        try:
            return cls(value)
        except ValueError:
            if not isinstance(value, str):
                raise
        unknown = str.__new__(cls, value)
        unknown._name_ = "UNKNOWN"
        unknown._value_ = value
        return unknown
