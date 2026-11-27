from enum import Enum


class CustodyDataRowData(str, Enum):
    ACCOUNT_IDENTITY = "account_identity"
    BROKER_PASSWORD = "broker_password"
    INSTRUMENT_NAMES = "instrument_names"
    TRADING_RECORDS = "trading_records"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CustodyDataRowData":
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
