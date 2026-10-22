from enum import Enum


class MdStatusMessageStatus(str, Enum):
    LIVE = "live"
    MAINTENANCE = "maintenance"

    def __str__(self) -> str:
        return str(self.value)
