from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_account_exposure_by_symbol_item import (
        RiskAccountExposureBySymbolItem,
    )


T = TypeVar("T", bound="RiskAccountExposure")


@_attrs_define
class RiskAccountExposure:
    """
    Attributes:
        gross (Union[None, str]):
        gross_limit (Union[None, str]):
        reserved (str): Held for entries whose outcome is not known yet
        by_symbol (list['RiskAccountExposureBySymbolItem']):
        positions (int):
        pending (int):
    """

    gross: Union[None, str]
    gross_limit: Union[None, str]
    reserved: str
    by_symbol: list["RiskAccountExposureBySymbolItem"]
    positions: int
    pending: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_account_exposure_by_symbol_item import (
            RiskAccountExposureBySymbolItem,
        )

        gross: Union[None, str]
        gross = self.gross

        gross_limit: Union[None, str]
        gross_limit = self.gross_limit

        reserved = self.reserved

        by_symbol = []
        for by_symbol_item_data in self.by_symbol:
            by_symbol_item = by_symbol_item_data.to_dict()
            by_symbol.append(by_symbol_item)

        positions = self.positions

        pending = self.pending

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gross": gross,
                "gross_limit": gross_limit,
                "reserved": reserved,
                "by_symbol": by_symbol,
                "positions": positions,
                "pending": pending,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_account_exposure_by_symbol_item import (
            RiskAccountExposureBySymbolItem,
        )

        d = dict(src_dict)

        def _parse_gross(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        gross = _parse_gross(d.pop("gross"))

        def _parse_gross_limit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        gross_limit = _parse_gross_limit(d.pop("gross_limit"))

        reserved = d.pop("reserved")

        by_symbol = []
        _by_symbol = d.pop("by_symbol")
        for by_symbol_item_data in _by_symbol:
            by_symbol_item = RiskAccountExposureBySymbolItem.from_dict(by_symbol_item_data)

            by_symbol.append(by_symbol_item)

        positions = d.pop("positions")

        pending = d.pop("pending")

        risk_account_exposure = cls(
            gross=gross,
            gross_limit=gross_limit,
            reserved=reserved,
            by_symbol=by_symbol,
            positions=positions,
            pending=pending,
        )

        risk_account_exposure.additional_properties = d
        return risk_account_exposure

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
