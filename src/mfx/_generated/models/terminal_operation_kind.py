from enum import Enum


class TerminalOperationKind(str, Enum):
    ATTACH = "attach"
    DETACH = "detach"
    DRAIN = "drain"
    MOVE = "move"
    REBUILD = "rebuild"
    RESTART = "restart"
    RETIRE = "retire"
    RETRY_LOGIN = "retry_login"
    SWAP = "swap"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "TerminalOperationKind":
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
