from enum import Enum


class EaTrialFigureKey(str, Enum):
    CPU_AVG = "cpu_avg"
    CPU_PEAK = "cpu_peak"
    DISK_WRITTEN = "disk_written"
    HEARTBEAT = "heartbeat"
    MEMORY_ADDED = "memory_added"
    OBJECTS_ADDED = "objects_added"
    ORDERS_PEAK = "orders_peak"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "EaTrialFigureKey":
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
