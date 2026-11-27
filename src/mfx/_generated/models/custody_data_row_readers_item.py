from enum import Enum


class CustodyDataRowReadersItem(str, Enum):
    ACCOUNT_SIGNED_IN = "account_signed_in"
    ATTESTED_MACHINE = "attested_machine"
    OPERATORS = "operators"
    YOU_THROUGH_THE_API = "you_through_the_api"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CustodyDataRowReadersItem":
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
