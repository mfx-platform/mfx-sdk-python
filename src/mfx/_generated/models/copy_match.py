from enum import Enum


class CopyMatch(str, Enum):
    AUTOMATIC = "automatic"
    INSTRUMENT_KEY = "instrument_key"
    OWN_MAP = "own_map"
    SAME_NAME = "same_name"

    def __str__(self) -> str:
        return str(self.value)
