from enum import Enum


class TerminalConditionChangedCondition(str, Enum):
    BROKERCONNECTED = "BrokerConnected"
    CREDENTIALLEASED = "CredentialLeased"
    PROCESSRUNNING = "ProcessRunning"
    TICKSFRESH = "TicksFresh"
    TRADEALLOWED = "TradeAllowed"

    def __str__(self) -> str:
        return str(self.value)
