from enum import Enum


class RiskCoverageDetectorType1(str, Enum):
    CELL = "cell"
    INGEST = "ingest"

    def __str__(self) -> str:
        return str(self.value)
