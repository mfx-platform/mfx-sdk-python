from enum import Enum


class PositionClosedCloseReason(str, Enum):
    CLIENT = "client"
    EXPERT = "expert"
    MOBILE = "mobile"
    ROLLOVER = "rollover"
    SL = "sl"
    SPLIT = "split"
    STOP_OUT = "stop_out"
    TP = "tp"
    UNKNOWN = "unknown"
    VMARGIN = "vmargin"
    WEB = "web"

    def __str__(self) -> str:
        return str(self.value)
