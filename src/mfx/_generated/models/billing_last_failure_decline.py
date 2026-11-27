from enum import Enum


class BillingLastFailureDecline(str, Enum):
    AUTHENTICATION_REQUIRED = "authentication_required"
    CARD_DECLINED = "card_declined"
    EXPIRED = "expired"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    OTHER = "other"
    PROCESSOR_ERROR = "processor_error"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "BillingLastFailureDecline":
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
