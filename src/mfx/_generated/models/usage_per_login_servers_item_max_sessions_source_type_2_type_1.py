from enum import Enum


class UsagePerLoginServersItemMaxSessionsSourceType2Type1(str, Enum):
    LIMIT = "limit"
    OPERATOR = "operator"
    PROBED = "probed"

    def __str__(self) -> str:
        return str(self.value)
