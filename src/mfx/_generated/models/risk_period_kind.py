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
