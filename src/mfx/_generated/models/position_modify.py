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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionModify")


@_attrs_define
class PositionModify:
    """At least one of sl and tp

    Attributes:
        sl (Union[Unset, str]): Decimal string; "0" clears it
        tp (Union[Unset, str]): Decimal string; "0" clears it
    """

    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        sl = self.sl

        tp = self.tp

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        position_modify = cls(
            sl=sl,
            tp=tp,
        )

        return position_modify
