from enum import Enum


class CopyCloseEntryWhyType1(str, Enum):
    COPY_MISMATCH = "copy_mismatch"
    GAVE_UP = "gave_up"
    NETTING = "netting"
    NOT_COPIED = "not_copied"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CopyCloseEntryWhyType1":
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
