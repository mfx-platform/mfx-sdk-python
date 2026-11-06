from enum import Enum


class RiskAccountOpenBreachesItemClears(str, Enum):
    AT_RESET = "at_reset"
    BY_OVERRIDE = "by_override"

    def __str__(self) -> str:
        return str(self.value)
