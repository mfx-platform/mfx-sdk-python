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

T = TypeVar("T", bound="CopyFollowerToday")


@_attrs_define
class CopyFollowerToday:
    """
    Attributes:
        copies (int): Its copy log rows of the current UTC day
        filled (int):
        mfx_ms_p50 (Union[None, float]): The median of MFX Hub's part of each copy; null when none has the stages
    """

    copies: int
    filled: int
    mfx_ms_p50: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        copies = self.copies

        filled = self.filled

        mfx_ms_p50: Union[None, float]
        mfx_ms_p50 = self.mfx_ms_p50

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "copies": copies,
                "filled": filled,
                "mfx_ms_p50": mfx_ms_p50,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        copies = d.pop("copies")

        filled = d.pop("filled")

        def _parse_mfx_ms_p50(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mfx_ms_p50 = _parse_mfx_ms_p50(d.pop("mfx_ms_p50"))

        copy_follower_today = cls(
            copies=copies,
            filled=filled,
            mfx_ms_p50=mfx_ms_p50,
        )

        copy_follower_today.additional_properties = d
        return copy_follower_today

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
