from enum import Enum


class TenantFarmRedundancy(str, Enum):
    ACTIVE_ACTIVE = "active_active"
    NONE = "none"
    N_PLUS_1 = "n_plus_1"

    def __str__(self) -> str:
        return str(self.value)
