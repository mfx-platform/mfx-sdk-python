from enum import Enum


class WebhookEndpointPausedByType3Type1(str, Enum):
    OPERATOR = "operator"
    PLATFORM = "platform"
    TENANT = "tenant"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "WebhookEndpointPausedByType3Type1":
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
