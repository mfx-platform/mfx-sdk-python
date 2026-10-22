from enum import Enum


class TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1(str, Enum):
    BROKER = "broker"

    def __str__(self) -> str:
        return str(self.value)
