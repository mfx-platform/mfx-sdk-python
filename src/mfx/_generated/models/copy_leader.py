import datetime
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
from dateutil.parser import isoparse

from ..models.copy_leader_source import CopyLeaderSource
from ..models.copy_leader_state import CopyLeaderState
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_leader_copies import CopyLeaderCopies
    from ..models.copy_leader_filters import CopyLeaderFilters
    from ..models.copy_leader_limits import CopyLeaderLimits
    from ..models.copy_who_may_join import CopyWhoMayJoin


T = TypeVar("T", bound="CopyLeader")


@_attrs_define
class CopyLeader:
    """
    Attributes:
        id (UUID):
        source (CopyLeaderSource): account: one of your accounts, whose fills are seen as they happen. external: a
            source that sends signals to the signals route
        account_id (Union[None, UUID]): The leader account; null for an external leader
        venue (Union[None, Venue]): The leader account's venue; null for an external leader
        filters (CopyLeaderFilters): Which of the leader's deals are copied. Nothing set copies every deal
        copies (CopyLeaderCopies): What of the leader's trading is copied
        signal_lifetime_s (int):
        limits (CopyLeaderLimits): Limits on the leader's own deals. A deal over one is copied to no follower, and every
            follower's log row says `refused` with reason `risk_rule`.
        who_may_join (CopyWhoMayJoin): Which of your accounts may follow this leader
        state (CopyLeaderState): active: its deals are copied. paused: its entries are not, its closes still are.
            retired: final
        followers_live (int): Followers that have not unfollowed
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    source: CopyLeaderSource
    account_id: Union[None, UUID]
    venue: Union[None, Venue]
    filters: "CopyLeaderFilters"
    copies: "CopyLeaderCopies"
    signal_lifetime_s: int
    limits: "CopyLeaderLimits"
    who_may_join: "CopyWhoMayJoin"
    state: CopyLeaderState
    followers_live: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_leader_copies import CopyLeaderCopies
        from ..models.copy_leader_filters import CopyLeaderFilters
        from ..models.copy_leader_limits import CopyLeaderLimits
        from ..models.copy_who_may_join import CopyWhoMayJoin

        id = str(self.id)

        source = self.source.value

        account_id: Union[None, str]
        if isinstance(self.account_id, UUID):
            account_id = str(self.account_id)
        else:
            account_id = self.account_id

        venue: Union[None, str]
        if isinstance(self.venue, Venue):
            venue = self.venue.value
        else:
            venue = self.venue

        filters = self.filters.to_dict()

        copies = self.copies.to_dict()

        signal_lifetime_s = self.signal_lifetime_s

        limits = self.limits.to_dict()

        who_may_join = self.who_may_join.to_dict()

        state = self.state.value

        followers_live = self.followers_live

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "source": source,
                "account_id": account_id,
                "venue": venue,
                "filters": filters,
                "copies": copies,
                "signal_lifetime_s": signal_lifetime_s,
                "limits": limits,
                "who_may_join": who_may_join,
                "state": state,
                "followers_live": followers_live,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_leader_copies import CopyLeaderCopies
        from ..models.copy_leader_filters import CopyLeaderFilters
        from ..models.copy_leader_limits import CopyLeaderLimits
        from ..models.copy_who_may_join import CopyWhoMayJoin

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        source = CopyLeaderSource(d.pop("source"))

        def _parse_account_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                account_id_type_0 = UUID(data)

                return account_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        account_id = _parse_account_id(d.pop("account_id"))

        def _parse_venue(data: object) -> Union[None, Venue]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                venue_type_0 = Venue(data)

                return venue_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Venue], data)

        venue = _parse_venue(d.pop("venue"))

        filters = CopyLeaderFilters.from_dict(d.pop("filters"))

        copies = CopyLeaderCopies.from_dict(d.pop("copies"))

        signal_lifetime_s = d.pop("signal_lifetime_s")

        limits = CopyLeaderLimits.from_dict(d.pop("limits"))

        who_may_join = CopyWhoMayJoin.from_dict(d.pop("who_may_join"))

        state = CopyLeaderState(d.pop("state"))

        followers_live = d.pop("followers_live")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        copy_leader = cls(
            id=id,
            source=source,
            account_id=account_id,
            venue=venue,
            filters=filters,
            copies=copies,
            signal_lifetime_s=signal_lifetime_s,
            limits=limits,
            who_may_join=who_may_join,
            state=state,
            followers_live=followers_live,
            created_at=created_at,
            updated_at=updated_at,
        )

        copy_leader.additional_properties = d
        return copy_leader

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
