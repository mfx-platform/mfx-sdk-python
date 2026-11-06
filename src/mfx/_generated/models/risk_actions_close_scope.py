from enum import Enum


class RiskActionsCloseScope(str, Enum):
    ALL_POSITIONS = "all_positions"
    MFX_POSITIONS = "mfx_positions"

    def __str__(self) -> str:
        return str(self.value)
