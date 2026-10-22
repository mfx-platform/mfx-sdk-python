from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrailingStopSet")


@_attrs_define
class TrailingStopSet:
    """Keep this position's stop loss `distance` behind the best price it reaches. The platform moves the broker's stop,
    only ever tighter, at most once a second and by at least a tenth of the distance. Setting again replaces the
    distance and keeps what the stop has reached. Refused with `invalid_request` when the ticket is not an open position
    of this account, and `invalid_stops` when the distance is inside the symbol's stops level.

        Attributes:
            distance (str): A price difference, a decimal string above zero, never a float
    """

    distance: str

    def to_dict(self) -> dict[str, Any]:
        distance = self.distance

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "distance": distance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        distance = d.pop("distance")

        trailing_stop_set = cls(
            distance=distance,
        )

        return trailing_stop_set
