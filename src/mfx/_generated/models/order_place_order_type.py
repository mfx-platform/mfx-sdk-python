from enum import Enum


class OrderPlaceOrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

    def __str__(self) -> str:
        return str(self.value)
