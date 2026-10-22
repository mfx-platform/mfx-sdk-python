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

T = TypeVar("T", bound="PositionClose")


@_attrs_define
class PositionClose:
    """
    Attributes:
        deviation_points (Union[Unset, int]):  Default: 20.
        comment (Union[Unset, str]): Written on the closing deal (Deal.comment), so a client can tell its own closes
            apart: every close the platform sends is MT5's close_reason expert, whoever asked for it. Absent, the closing
            deal takes the position's own comment. MT5 cuts anything longer without saying so, so longer is refused
    """

    deviation_points: Union[Unset, int] = 20
    comment: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        deviation_points = self.deviation_points

        comment = self.comment

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if deviation_points is not UNSET:
            field_dict["deviation_points"] = deviation_points
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deviation_points = d.pop("deviation_points", UNSET)

        comment = d.pop("comment", UNSET)

        position_close = cls(
            deviation_points=deviation_points,
            comment=comment,
        )

        return position_close
