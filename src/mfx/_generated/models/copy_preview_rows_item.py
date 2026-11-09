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

from ..models.copy_match import CopyMatch
from ..models.copy_reason import CopyReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyPreviewRowsItem")


@_attrs_define
class CopyPreviewRowsItem:
    """
    Attributes:
        leader_symbol (str):
        leader_volume (str):
        instrument_key (Union[None, str]):
        follower_symbol (Union[None, str]): Null when no symbol matched
        matched_by (Union[CopyMatch, None]):
        follower_volume (Union[None, str]): In the follower venue's unit; null when refused
        reason (Union[CopyReason, None]): Why this row would be refused; null when it would be copied
    """

    leader_symbol: str
    leader_volume: str
    instrument_key: Union[None, str]
    follower_symbol: Union[None, str]
    matched_by: Union[CopyMatch, None]
    follower_volume: Union[None, str]
    reason: Union[CopyReason, None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        leader_symbol = self.leader_symbol

        leader_volume = self.leader_volume

        instrument_key: Union[None, str]
        instrument_key = self.instrument_key

        follower_symbol: Union[None, str]
        follower_symbol = self.follower_symbol

        matched_by: Union[None, str]
        if isinstance(self.matched_by, CopyMatch):
            matched_by = self.matched_by.value
        else:
            matched_by = self.matched_by

        follower_volume: Union[None, str]
        follower_volume = self.follower_volume

        reason: Union[None, str]
        if isinstance(self.reason, CopyReason):
            reason = self.reason.value
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "leader_symbol": leader_symbol,
                "leader_volume": leader_volume,
                "instrument_key": instrument_key,
                "follower_symbol": follower_symbol,
                "matched_by": matched_by,
                "follower_volume": follower_volume,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        leader_symbol = d.pop("leader_symbol")

        leader_volume = d.pop("leader_volume")

        def _parse_instrument_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instrument_key = _parse_instrument_key(d.pop("instrument_key"))

        def _parse_follower_symbol(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_symbol = _parse_follower_symbol(d.pop("follower_symbol"))

        def _parse_matched_by(data: object) -> Union[CopyMatch, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                matched_by_type_0 = CopyMatch(data)

                return matched_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CopyMatch, None], data)

        matched_by = _parse_matched_by(d.pop("matched_by"))

        def _parse_follower_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_volume = _parse_follower_volume(d.pop("follower_volume"))

        def _parse_reason(data: object) -> Union[CopyReason, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_0 = CopyReason(data)

                return reason_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CopyReason, None], data)

        reason = _parse_reason(d.pop("reason"))

        copy_preview_rows_item = cls(
            leader_symbol=leader_symbol,
            leader_volume=leader_volume,
            instrument_key=instrument_key,
            follower_symbol=follower_symbol,
            matched_by=matched_by,
            follower_volume=follower_volume,
            reason=reason,
        )

        copy_preview_rows_item.additional_properties = d
        return copy_preview_rows_item

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
