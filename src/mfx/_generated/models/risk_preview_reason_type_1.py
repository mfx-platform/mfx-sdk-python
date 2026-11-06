from enum import Enum


class RiskPreviewReasonType1(str, Enum):
    VOLUME_MIN_OVER_BUDGET = "volume_min_over_budget"

    def __str__(self) -> str:
        return str(self.value)
