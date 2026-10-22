from enum import Enum


class TenantFarmUsagesItem(str, Enum):
    ACCOUNT_READ = "account_read"
    ORDER_EXECUTION = "order_execution"
    QUOTE_STREAMING = "quote_streaming"

    def __str__(self) -> str:
        return str(self.value)
