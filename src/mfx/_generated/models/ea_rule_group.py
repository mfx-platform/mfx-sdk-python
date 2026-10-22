from enum import Enum


class EaRuleGroup(str, Enum):
    BEST_PRACTICE = "best_practice"
    CONTRACT_BUILD = "contract_build"
    INTERFACE = "interface"
    PERFORMANCE = "performance"
    SECURITY = "security"
    THREAT = "threat"
    TRADING = "trading"

    def __str__(self) -> str:
        return str(self.value)
