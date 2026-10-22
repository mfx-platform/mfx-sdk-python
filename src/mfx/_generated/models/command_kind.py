from enum import Enum


class CommandKind(str, Enum):
    ORDER_CANCEL = "order_cancel"
    ORDER_MODIFY = "order_modify"
    ORDER_PLACE = "order_place"
    POSITION_CLOSE = "position_close"
    POSITION_CLOSE_BY = "position_close_by"
    POSITION_CLOSE_PARTIAL = "position_close_partial"
    POSITION_MODIFY = "position_modify"
    TRAILING_STOP_CLEAR = "trailing_stop_clear"
    TRAILING_STOP_SET = "trailing_stop_set"

    def __str__(self) -> str:
        return str(self.value)
