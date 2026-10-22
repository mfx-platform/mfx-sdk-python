from enum import Enum


class DealCloseReasonType2Type1(str, Enum):
    CLIENT = "client"
    EXPERT = "expert"
    MOBILE = "mobile"
    ROLLOVER = "rollover"
    SL = "sl"
    SPLIT = "split"
    STOP_OUT = "stop_out"
    TP = "tp"
    VMARGIN = "vmargin"
    WEB = "web"

    def __str__(self) -> str:
        return str(self.value)
