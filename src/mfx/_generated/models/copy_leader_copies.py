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

T = TypeVar("T", bound="CopyLeaderCopies")


@_attrs_define
class CopyLeaderCopies:
    """What of the leader's trading is copied

    Attributes:
        entries (Union[Unset, bool]):  Default: True.
        pending (Union[Unset, bool]): The leader's pending orders, placed, changed and cancelled Default: True.
        sl (Union[Unset, bool]):  Default: True.
        tp (Union[Unset, bool]):  Default: True.
        modifications (Union[Unset, bool]): Changes to the stop loss and take profit of an open position Default: True.
        partial_closes (Union[Unset, bool]):  Default: True.
        close_only (Union[Unset, bool]): Copy closes only: no follower opens anything new from this leader Default:
            False.
    """

    entries: Union[Unset, bool] = True
    pending: Union[Unset, bool] = True
    sl: Union[Unset, bool] = True
    tp: Union[Unset, bool] = True
    modifications: Union[Unset, bool] = True
    partial_closes: Union[Unset, bool] = True
    close_only: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        entries = self.entries

        pending = self.pending

        sl = self.sl

        tp = self.tp

        modifications = self.modifications

        partial_closes = self.partial_closes

        close_only = self.close_only

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if entries is not UNSET:
            field_dict["entries"] = entries
        if pending is not UNSET:
            field_dict["pending"] = pending
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if modifications is not UNSET:
            field_dict["modifications"] = modifications
        if partial_closes is not UNSET:
            field_dict["partial_closes"] = partial_closes
        if close_only is not UNSET:
            field_dict["close_only"] = close_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entries = d.pop("entries", UNSET)

        pending = d.pop("pending", UNSET)

        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        modifications = d.pop("modifications", UNSET)

        partial_closes = d.pop("partial_closes", UNSET)

        close_only = d.pop("close_only", UNSET)

        copy_leader_copies = cls(
            entries=entries,
            pending=pending,
            sl=sl,
            tp=tp,
            modifications=modifications,
            partial_closes=partial_closes,
            close_only=close_only,
        )

        return copy_leader_copies
