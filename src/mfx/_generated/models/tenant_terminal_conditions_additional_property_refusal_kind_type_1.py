from enum import Enum


class TenantTerminalConditionsAdditionalPropertyRefusalKindType1(str, Enum):
    INVALID_ACCOUNT = "invalid_account"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
