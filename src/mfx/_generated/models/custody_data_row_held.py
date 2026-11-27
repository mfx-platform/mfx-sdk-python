from enum import Enum


class CustodyDataRowHeld(str, Enum):
    ENCRYPTED_UNDER_YOUR_KEY = "encrypted_under_your_key"
    IN_CLEAR = "in_clear"
    VAULT_RELEASED_TO_ATTESTED_MACHINE = "vault_released_to_attested_machine"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CustodyDataRowHeld":
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
