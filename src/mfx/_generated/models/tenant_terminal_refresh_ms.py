from enum import IntEnum


class TenantTerminalRefreshMs(IntEnum):
    VALUE_5000 = 5000
    VALUE_4000 = 4000
    VALUE_3000 = 3000
    VALUE_2000 = 2000
    VALUE_1000 = 1000
    VALUE_500 = 500
    VALUE_250 = 250
    VALUE_200 = 200

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: int) -> "TenantTerminalRefreshMs":
        """A number from a response: its member, or, for a number a later version of the API
        added, an UNKNOWN pseudo-member whose value is the number as sent."""
        try:
            return cls(value)
        except ValueError:
            if not isinstance(value, int) or isinstance(value, bool):
                raise
        unknown = int.__new__(cls, value)
        unknown._name_ = "UNKNOWN"
        unknown._value_ = value
        return unknown
