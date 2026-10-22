from enum import Enum


class TenantFarmOs(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"

    def __str__(self) -> str:
        return str(self.value)
