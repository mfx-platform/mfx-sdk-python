from enum import Enum


class RiskDrawdownPeakWhen(str, Enum):
    END_OF_DAY = "end_of_day"
    INTRADAY = "intraday"

    def __str__(self) -> str:
        return str(self.value)
