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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.copy_leader_source import CopyLeaderSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_leader_copies import CopyLeaderCopies
    from ..models.copy_leader_filters import CopyLeaderFilters
    from ..models.copy_leader_limits import CopyLeaderLimits
    from ..models.copy_who_may_join import CopyWhoMayJoin


T = TypeVar("T", bound="CopyLeaderCreate")


@_attrs_define
class CopyLeaderCreate:
    """
    Attributes:
        source (CopyLeaderSource): account: one of your accounts, whose fills are seen as they happen. external: a
            source that sends signals to the signals route
        signal_lifetime_s (int): How long a signal may still be copied after MFX Hub makes it, in seconds. A follower
            that cannot act on it in time logs signal_expired. You set it; MFX Hub suggests none
        account_id (Union[None, UUID, Unset]): The account (an /accounts id) when source is account; absent or null when
            external
        filters (Union[Unset, CopyLeaderFilters]): Which of the leader's deals are copied. Nothing set copies every deal
        copies (Union[Unset, CopyLeaderCopies]): What of the leader's trading is copied
        limits (Union[Unset, CopyLeaderLimits]): Limits on the leader's own deals. A deal over one is copied to no
            follower, and every follower's log row says `refused` with reason `risk_rule`.
        who_may_join (Union[Unset, CopyWhoMayJoin]): Which of your accounts may follow this leader
    """

    source: CopyLeaderSource
    signal_lifetime_s: int
    account_id: Union[None, UUID, Unset] = UNSET
    filters: Union[Unset, "CopyLeaderFilters"] = UNSET
    copies: Union[Unset, "CopyLeaderCopies"] = UNSET
    limits: Union[Unset, "CopyLeaderLimits"] = UNSET
    who_may_join: Union[Unset, "CopyWhoMayJoin"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_leader_copies import CopyLeaderCopies
        from ..models.copy_leader_filters import CopyLeaderFilters
        from ..models.copy_leader_limits import CopyLeaderLimits
        from ..models.copy_who_may_join import CopyWhoMayJoin

        source = self.source.value

        signal_lifetime_s = self.signal_lifetime_s

        account_id: Union[None, Unset, str]
        if isinstance(self.account_id, Unset):
            account_id = UNSET
        elif isinstance(self.account_id, UUID):
            account_id = str(self.account_id)
        else:
            account_id = self.account_id

        filters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        copies: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.copies, Unset):
            copies = self.copies.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        who_may_join: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.who_may_join, Unset):
            who_may_join = self.who_may_join.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "signal_lifetime_s": signal_lifetime_s,
            }
        )
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if copies is not UNSET:
            field_dict["copies"] = copies
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
        source = CopyLeaderSource(d.pop("source"))

        signal_lifetime_s = d.pop("signal_lifetime_s")

        def _parse_account_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                account_id_type_0 = UUID(data)

                return account_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        account_id = _parse_account_id(d.pop("account_id", UNSET))

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

        copy_leader_create = cls(
            source=source,
            signal_lifetime_s=signal_lifetime_s,
            account_id=account_id,
            filters=filters,
            copies=copies,
            limits=limits,
            who_may_join=who_may_join,
        )

        return copy_leader_create
