from enum import Enum


class MaintenanceService(str, Enum):
    EXPERT_ADVISORS = "expert_advisors"
    FARM_CREATION = "farm_creation"
    FARM_MANAGEMENT = "farm_management"
    MARKET_DATA = "market_data"
    ORDER_PLACEMENT = "order_placement"
    TENANT_CONSOLE_READ_ONLY = "tenant_console_read_only"
    TENANT_CONSOLE_UNAVAILABLE = "tenant_console_unavailable"
    TERMINAL_CREATION = "terminal_creation"
    TERMINAL_LOGINS = "terminal_logins"
    TERMINAL_MANAGEMENT = "terminal_management"

    def __str__(self) -> str:
        return str(self.value)
