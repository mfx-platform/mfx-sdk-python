from enum import Enum


class CopyScalingMode(str, Enum):
    BALANCE_RATIO = "balance_ratio"
    CONTRACT_SIZE = "contract_size"
    EQUITY_RATIO = "equity_ratio"
    FIXED_MULTIPLIER = "fixed_multiplier"
    FIXED_RISK = "fixed_risk"
    FIXED_VOLUME = "fixed_volume"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CopyScalingMode":
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
