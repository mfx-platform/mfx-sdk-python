from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionCloseBy")


@_attrs_define
class PositionCloseBy:
    """Close the position in the path against an opposite position in the same symbol. Hedging accounts only: the smaller
    position disappears and the larger is reduced by its volume. Refused with `invalid_request`, before the broker, when
    either ticket is not an open position of this account, when the two are in different symbols or on the same side, or
    when they are the same ticket.

        Attributes:
            by_ticket (int): The opposite position's ticket
    """

    by_ticket: int

    def to_dict(self) -> dict[str, Any]:
        by_ticket = self.by_ticket

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "by_ticket": by_ticket,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        by_ticket = d.pop("by_ticket")

        position_close_by = cls(
            by_ticket=by_ticket,
        )

        return position_close_by
