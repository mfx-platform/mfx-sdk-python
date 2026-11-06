from enum import Enum


class RiskActionsCancelScope(str, Enum):
    ALL_PENDING = "all_pending"
    MFX_PENDING = "mfx_pending"

    def __str__(self) -> str:
        return str(self.value)
