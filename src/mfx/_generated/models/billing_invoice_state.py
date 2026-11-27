from enum import Enum


class BillingInvoiceState(str, Enum):
    DUE = "due"
    ISSUED = "issued"
    OVERDUE = "overdue"
    PART_SETTLED = "part_settled"
    SETTLED = "settled"
    SETTLEMENT_IN_PROGRESS = "settlement_in_progress"
    VOID = "void"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "BillingInvoiceState":
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
