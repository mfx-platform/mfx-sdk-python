from enum import IntEnum


class TenantTerminalRefreshMs(IntEnum):
    VALUE_5000 = 5000
    VALUE_4000 = 4000
    VALUE_3000 = 3000
    VALUE_2000 = 2000
    VALUE_1000 = 1000
    VALUE_500 = 500
    VALUE_250 = 250
    VALUE_200 = 200

    def __str__(self) -> str:
        return str(self.value)
