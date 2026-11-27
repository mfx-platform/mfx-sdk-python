from enum import Enum


class RiskPeriodKind(str, Enum):
    DATE = "date"
    DAY = "day"
    LIFETIME = "lifetime"
    MONTH = "month"
    MONTH_TO_DATE = "month-to-date"
    QUARTER = "quarter"
    QUARTER_TO_DATE = "quarter-to-date"
    WEEK = "week"
    WEEK_TO_DATE = "week-to-date"
    YEAR = "year"
    YEAR_TO_DATE = "year-to-date"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "RiskPeriodKind":
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
