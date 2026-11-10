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

T = TypeVar("T", bound="TradingSymbol")


@_attrs_define
class TradingSymbol:
    """One symbol of a cTrader account, as Spotware gives it for that account.

    Attributes:
        name (str): The broker's own name, as commands take it
        symbol_id (int): cTrader's id of the symbol
        digits (int): Decimals of its price
        pip_position (int):
        lot_size (str): Units of the base asset in one lot, as a decimal string
        volume_step (str): Lots, as a decimal string
        volume_min (str): Lots
        volume_max (Union[None, str]): Lots; null when the broker states none
        leverage (Union[None, int]): The leverage of the smallest tier, as 1:N; null when the broker names none
        margin_rate (Union[None, str]): 1 / leverage, the share of the notional held as margin at that tier
        base_asset (Union[None, str]):
        quote_asset (Union[None, str]):
        enabled (bool):
    """

    name: str
    symbol_id: int
    digits: int
    pip_position: int
    lot_size: str
    volume_step: str
    volume_min: str
    volume_max: Union[None, str]
    leverage: Union[None, int]
    margin_rate: Union[None, str]
    base_asset: Union[None, str]
    quote_asset: Union[None, str]
    enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        symbol_id = self.symbol_id

        digits = self.digits

        pip_position = self.pip_position

        lot_size = self.lot_size

        volume_step = self.volume_step

        volume_min = self.volume_min

        volume_max: Union[None, str]
        volume_max = self.volume_max

        leverage: Union[None, int]
        leverage = self.leverage

        margin_rate: Union[None, str]
        margin_rate = self.margin_rate

        base_asset: Union[None, str]
        base_asset = self.base_asset

        quote_asset: Union[None, str]
        quote_asset = self.quote_asset

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "symbol_id": symbol_id,
                "digits": digits,
                "pip_position": pip_position,
                "lot_size": lot_size,
                "volume_step": volume_step,
                "volume_min": volume_min,
                "volume_max": volume_max,
                "leverage": leverage,
                "margin_rate": margin_rate,
                "base_asset": base_asset,
                "quote_asset": quote_asset,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        symbol_id = d.pop("symbol_id")

        digits = d.pop("digits")

        pip_position = d.pop("pip_position")

        lot_size = d.pop("lot_size")

        volume_step = d.pop("volume_step")

        volume_min = d.pop("volume_min")

        def _parse_volume_max(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume_max = _parse_volume_max(d.pop("volume_max"))

        def _parse_leverage(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        leverage = _parse_leverage(d.pop("leverage"))

        def _parse_margin_rate(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        margin_rate = _parse_margin_rate(d.pop("margin_rate"))

        def _parse_base_asset(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        base_asset = _parse_base_asset(d.pop("base_asset"))

        def _parse_quote_asset(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        quote_asset = _parse_quote_asset(d.pop("quote_asset"))

        enabled = d.pop("enabled")

        trading_symbol = cls(
            name=name,
            symbol_id=symbol_id,
            digits=digits,
            pip_position=pip_position,
            lot_size=lot_size,
            volume_step=volume_step,
            volume_min=volume_min,
            volume_max=volume_max,
            leverage=leverage,
            margin_rate=margin_rate,
            base_asset=base_asset,
            quote_asset=quote_asset,
            enabled=enabled,
        )

        trading_symbol.additional_properties = d
        return trading_symbol

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
