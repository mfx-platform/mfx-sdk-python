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

    @classmethod
    def _read(cls, value: str) -> "EaRuleGroup":
        """A word from a response: its member, or, for a word a later version of the API added,
        an UNKNOWN pseudo-member whose value is the word as sent."""
        try:
            return cls(value)
        except ValueError:
            if not isinstance(value, str):
                raise
        unknown = str.__new__(cls, value)
        unknown._name_ = "UNKNOWN"
        unknown._value_ = value
        return unknown
