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

if TYPE_CHECKING:
    from ..models.copy_leader_copies import CopyLeaderCopies
    from ..models.copy_leader_filters import CopyLeaderFilters
    from ..models.copy_leader_limits import CopyLeaderLimits
    from ..models.copy_who_may_join import CopyWhoMayJoin


T = TypeVar("T", bound="CopyLeaderUpdate")


@_attrs_define
class CopyLeaderUpdate:
    """
    Attributes:
        filters (Union[Unset, CopyLeaderFilters]): Which of the leader's deals are copied. Nothing set copies every deal
        copies (Union[Unset, CopyLeaderCopies]): What of the leader's trading is copied
        signal_lifetime_s (Union[Unset, int]):
        limits (Union[Unset, CopyLeaderLimits]): Limits on the leader's own deals. A deal over one is copied to no
            follower, and every follower's log row says `refused` with reason `risk_rule`.
        who_may_join (Union[Unset, CopyWhoMayJoin]): Which of your accounts may follow this leader
    """

    filters: Union[Unset, "CopyLeaderFilters"] = UNSET
    copies: Union[Unset, "CopyLeaderCopies"] = UNSET
    signal_lifetime_s: Union[Unset, int] = UNSET
    limits: Union[Unset, "CopyLeaderLimits"] = UNSET
    who_may_join: Union[Unset, "CopyWhoMayJoin"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_leader_copies import CopyLeaderCopies
        from ..models.copy_leader_filters import CopyLeaderFilters
        from ..models.copy_leader_limits import CopyLeaderLimits
        from ..models.copy_who_may_join import CopyWhoMayJoin

        filters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        copies: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.copies, Unset):
            copies = self.copies.to_dict()

        signal_lifetime_s = self.signal_lifetime_s

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        who_may_join: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.who_may_join, Unset):
            who_may_join = self.who_may_join.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if copies is not UNSET:
            field_dict["copies"] = copies
        if signal_lifetime_s is not UNSET:
            field_dict["signal_lifetime_s"] = signal_lifetime_s
        if limits is not UNSET:
            field_dict["limits"] = limits
        if who_may_join is not UNSET:
            field_dict["who_may_join"] = who_may_join

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_leader_copies import CopyLeaderCopies
        from ..models.copy_leader_filters import CopyLeaderFilters
        from ..models.copy_leader_limits import CopyLeaderLimits
        from ..models.copy_who_may_join import CopyWhoMayJoin

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: Union[Unset, CopyLeaderFilters]
        if isinstance(_filters, Unset):
            filters = UNSET
        else:
            filters = CopyLeaderFilters.from_dict(_filters)

        _copies = d.pop("copies", UNSET)
        copies: Union[Unset, CopyLeaderCopies]
        if isinstance(_copies, Unset):
            copies = UNSET
        else:
            copies = CopyLeaderCopies.from_dict(_copies)

        signal_lifetime_s = d.pop("signal_lifetime_s", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, CopyLeaderLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = CopyLeaderLimits.from_dict(_limits)

        _who_may_join = d.pop("who_may_join", UNSET)
        who_may_join: Union[Unset, CopyWhoMayJoin]
        if isinstance(_who_may_join, Unset):
            who_may_join = UNSET
        else:
            who_may_join = CopyWhoMayJoin.from_dict(_who_may_join)

        copy_leader_update = cls(
            filters=filters,
            copies=copies,
            signal_lifetime_s=signal_lifetime_s,
            limits=limits,
            who_may_join=who_may_join,
        )

        return copy_leader_update
