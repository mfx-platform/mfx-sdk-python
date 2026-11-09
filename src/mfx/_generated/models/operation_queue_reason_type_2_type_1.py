from enum import Enum


class OperationQueueReasonType2Type1(str, Enum):
    BACKOFF = "backoff"
    BROKER_BUDGET = "broker_budget"
    BROKER_CAP = "broker_cap"
    BROKER_MAINTENANCE = "broker_maintenance"
    BULK_PACE = "bulk_pace"
    CELL_AT_STOP_LINE = "cell_at_stop_line"
    CELL_BUSY = "cell_busy"
    CELL_SETTLING = "cell_settling"
    CELL_SILENT = "cell_silent"
    PLATFORM_CEILING = "platform_ceiling"

    def __str__(self) -> str:
        return str(self.value)
