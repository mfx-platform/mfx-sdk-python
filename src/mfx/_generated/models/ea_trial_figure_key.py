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
