from enum import Enum


class CopyScalingMode(str, Enum):
    BALANCE_RATIO = "balance_ratio"
    CONTRACT_SIZE = "contract_size"
    EQUITY_RATIO = "equity_ratio"
    FIXED_MULTIPLIER = "fixed_multiplier"
    FIXED_RISK = "fixed_risk"
    FIXED_VOLUME = "fixed_volume"

    def __str__(self) -> str:
        return str(self.value)
