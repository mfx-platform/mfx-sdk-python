from enum import Enum


class SymbolFillingModesType0Item(str, Enum):
    BOC = "boc"
    FOK = "fok"
    IOC = "ioc"

    def __str__(self) -> str:
        return str(self.value)
