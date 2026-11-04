from enum import Enum


class BrokerCatalogueSource(str, Enum):
    LAST_KNOWN = "last_known"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
