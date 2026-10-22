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

T = TypeVar("T", bound="PositionClosePartial")


@_attrs_define
class PositionClosePartial:
    """
    Attributes:
        volume (str): Lots to close, as a decimal string above zero; less than the position and on the symbol's step.
            Snapped onto the step first, then compared against the position, so the volume judged is the volume sent
        deviation_points (Union[Unset, int]):  Default: 20.
        comment (Union[Unset, str]): Written on the closing deal, as on PositionClose; absent, the deal takes the
            position's own comment. The position keeps its own comment. Longer than 31 characters is refused
    """

    volume: str
    deviation_points: Union[Unset, int] = 20
    comment: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        volume = self.volume

        deviation_points = self.deviation_points

        comment = self.comment

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "volume": volume,
            }
        )
        if deviation_points is not UNSET:
            field_dict["deviation_points"] = deviation_points
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        volume = d.pop("volume")

        deviation_points = d.pop("deviation_points", UNSET)

        comment = d.pop("comment", UNSET)

        position_close_partial = cls(
            volume=volume,
            deviation_points=deviation_points,
            comment=comment,
        )

        return position_close_partial
