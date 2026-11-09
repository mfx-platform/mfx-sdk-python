from enum import Enum


class ListCopyLogSort(str, Enum):
    CREATED_AT = "created_at"
    MFX_MS = "mfx_ms"

    def __str__(self) -> str:
        return str(self.value)
