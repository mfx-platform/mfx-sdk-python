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

from ..models.risk_close_scope_positions_item_side import (
    RiskCloseScopePositionsItemSide,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskCloseScopePositionsItem")


@_attrs_define
class RiskCloseScopePositionsItem:
    """
    Attributes:
        ticket (str):
        symbol (str):
        side (RiskCloseScopePositionsItemSide):
        volume (Union[None, str]):
        profit (Union[None, str]):
        placed_by_mfx (bool): Opened by an order MFX Hub placed; mfx_positions reaches only these
    """

    ticket: str
    symbol: str
    side: RiskCloseScopePositionsItemSide
    volume: Union[None, str]
    profit: Union[None, str]
    placed_by_mfx: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket = self.ticket

        symbol = self.symbol

        side = self.side.value

        volume: Union[None, str]
        volume = self.volume

        profit: Union[None, str]
        profit = self.profit

        placed_by_mfx = self.placed_by_mfx

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
                "symbol": symbol,
                "side": side,
                "volume": volume,
                "profit": profit,
                "placed_by_mfx": placed_by_mfx,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket = d.pop("ticket")

        symbol = d.pop("symbol")

        side = RiskCloseScopePositionsItemSide._read(d.pop("side"))

        def _parse_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume = _parse_volume(d.pop("volume"))

        def _parse_profit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profit = _parse_profit(d.pop("profit"))

        placed_by_mfx = d.pop("placed_by_mfx")

        risk_close_scope_positions_item = cls(
            ticket=ticket,
            symbol=symbol,
            side=side,
            volume=volume,
            profit=profit,
            placed_by_mfx=placed_by_mfx,
        )

        risk_close_scope_positions_item.additional_properties = d
        return risk_close_scope_positions_item

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
