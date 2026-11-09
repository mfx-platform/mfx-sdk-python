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

T = TypeVar("T", bound="CopyBounds")


@_attrs_define
class CopyBounds:
    """The follower's own limits on one copy, in its venue's unit; the broker's apply as well, and the tighter wins

    Attributes:
        min_volume (Union[None, Unset, str]): Under it a copy is refused with min_volume, never enlarged
        max_volume (Union[None, Unset, str]): Over it a copy is cut to it
        max_open (Union[None, Unset, int]): The most positions copied from this leader open at once; a copy over it is
            refused with risk_rule
    """

    min_volume: Union[None, Unset, str] = UNSET
    max_volume: Union[None, Unset, str] = UNSET
    max_open: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        min_volume: Union[None, Unset, str]
        if isinstance(self.min_volume, Unset):
            min_volume = UNSET
        else:
            min_volume = self.min_volume

        max_volume: Union[None, Unset, str]
        if isinstance(self.max_volume, Unset):
            max_volume = UNSET
        else:
            max_volume = self.max_volume

        max_open: Union[None, Unset, int]
        if isinstance(self.max_open, Unset):
            max_open = UNSET
        else:
            max_open = self.max_open

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if min_volume is not UNSET:
            field_dict["min_volume"] = min_volume
        if max_volume is not UNSET:
            field_dict["max_volume"] = max_volume
        if max_open is not UNSET:
            field_dict["max_open"] = max_open

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_min_volume(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        min_volume = _parse_min_volume(d.pop("min_volume", UNSET))

        def _parse_max_volume(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_volume = _parse_max_volume(d.pop("max_volume", UNSET))

        def _parse_max_open(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_open = _parse_max_open(d.pop("max_open", UNSET))

        copy_bounds = cls(
            min_volume=min_volume,
            max_volume=max_volume,
            max_open=max_open,
        )

        return copy_bounds
