from enum import Enum


class TradeSessionDay(str, Enum):
    FRI = "fri"
    MON = "mon"
    SAT = "sat"
    SUN = "sun"
    THU = "thu"
    TUE = "tue"
    WED = "wed"

    def __str__(self) -> str:
        return str(self.value)
