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
from ..models.copy_preview_rows_item_follower_volume_unit_type_1 import (
    CopyPreviewRowsItemFollowerVolumeUnitType1,
)
from ..models.copy_preview_rows_item_follower_volume_unit_type_2_type_1 import (
    CopyPreviewRowsItemFollowerVolumeUnitType2Type1,
)
from ..models.copy_preview_rows_item_follower_volume_unit_type_3_type_1 import (
    CopyPreviewRowsItemFollowerVolumeUnitType3Type1,
)
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
        leader_contract_size (Union[None, str]): The leader symbol's contract as the row was worked from it: a lot's
            size for a symbol in lots, 1 for one counted in units; null when the leader's symbol was not found
        follower_contract_size (Union[None, str]): The follower symbol's contract, as leader_contract_size; null when no
            symbol matched
        follower_volume_unit (Union[CopyPreviewRowsItemFollowerVolumeUnitType1,
            CopyPreviewRowsItemFollowerVolumeUnitType2Type1, CopyPreviewRowsItemFollowerVolumeUnitType3Type1, None]): The
            unit follower_volume is in; null when no symbol matched
    """

    leader_symbol: str
    leader_volume: str
    instrument_key: Union[None, str]
    follower_symbol: Union[None, str]
    matched_by: Union[CopyMatch, None]
    follower_volume: Union[None, str]
    reason: Union[CopyReason, None]
    leader_contract_size: Union[None, str]
    follower_contract_size: Union[None, str]
    follower_volume_unit: Union[
        CopyPreviewRowsItemFollowerVolumeUnitType1,
        CopyPreviewRowsItemFollowerVolumeUnitType2Type1,
        CopyPreviewRowsItemFollowerVolumeUnitType3Type1,
        None,
    ]
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

        leader_contract_size: Union[None, str]
        leader_contract_size = self.leader_contract_size

        follower_contract_size: Union[None, str]
        follower_contract_size = self.follower_contract_size

        follower_volume_unit: Union[None, str]
        if isinstance(self.follower_volume_unit, CopyPreviewRowsItemFollowerVolumeUnitType1):
            follower_volume_unit = self.follower_volume_unit.value
        elif isinstance(self.follower_volume_unit, CopyPreviewRowsItemFollowerVolumeUnitType2Type1):
            follower_volume_unit = self.follower_volume_unit.value
        elif isinstance(self.follower_volume_unit, CopyPreviewRowsItemFollowerVolumeUnitType3Type1):
            follower_volume_unit = self.follower_volume_unit.value
        else:
            follower_volume_unit = self.follower_volume_unit

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
                "leader_contract_size": leader_contract_size,
                "follower_contract_size": follower_contract_size,
                "follower_volume_unit": follower_volume_unit,
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
                matched_by_type_0 = CopyMatch._read(data)

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
                reason_type_0 = CopyReason._read(data)

                return reason_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CopyReason, None], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_leader_contract_size(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        leader_contract_size = _parse_leader_contract_size(d.pop("leader_contract_size"))

        def _parse_follower_contract_size(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_contract_size = _parse_follower_contract_size(d.pop("follower_contract_size"))

        def _parse_follower_volume_unit(
            data: object,
        ) -> Union[
            CopyPreviewRowsItemFollowerVolumeUnitType1,
            CopyPreviewRowsItemFollowerVolumeUnitType2Type1,
            CopyPreviewRowsItemFollowerVolumeUnitType3Type1,
            None,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                follower_volume_unit_type_1 = CopyPreviewRowsItemFollowerVolumeUnitType1._read(data)

                return follower_volume_unit_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                follower_volume_unit_type_2_type_1 = (
                    CopyPreviewRowsItemFollowerVolumeUnitType2Type1._read(data)
                )

                return follower_volume_unit_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                follower_volume_unit_type_3_type_1 = (
                    CopyPreviewRowsItemFollowerVolumeUnitType3Type1._read(data)
                )

                return follower_volume_unit_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    CopyPreviewRowsItemFollowerVolumeUnitType1,
                    CopyPreviewRowsItemFollowerVolumeUnitType2Type1,
                    CopyPreviewRowsItemFollowerVolumeUnitType3Type1,
                    None,
                ],
                data,
            )

        follower_volume_unit = _parse_follower_volume_unit(d.pop("follower_volume_unit"))

        copy_preview_rows_item = cls(
            leader_symbol=leader_symbol,
            leader_volume=leader_volume,
            instrument_key=instrument_key,
            follower_symbol=follower_symbol,
            matched_by=matched_by,
            follower_volume=follower_volume,
            reason=reason,
            leader_contract_size=leader_contract_size,
            follower_contract_size=follower_contract_size,
            follower_volume_unit=follower_volume_unit,
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
