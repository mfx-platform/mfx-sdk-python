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

from ..models.copy_close_cause import CopyCloseCause
from ..models.copy_close_state import CopyCloseState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_close_entry import CopyCloseEntry


T = TypeVar("T", bound="CopyClose")


@_attrs_define
class CopyClose:
    """A requested close of one follower's copied positions: asked by `unfollowCopyLeader` or `retireCopyLeader` with
    `close_copied`, or by a group's close, and carried to the account's copy host in the follower's signed mandate. Only
    the volume copied from the leader is closed, never the account's own. A refusal that says nothing was done (a market
    closed, a broker error) is tried again, waiting twice as long each time up to 15 minutes, until the close is given
    up (72 hours by default); an order with no answer is never tried blind: the account's positions decide.

        Attributes:
            id (UUID):
            follower_id (UUID):
            leader_id (UUID):
            account_id (UUID): The follower account
            group_id (Union[None, UUID]): The group, for a group's close
            batch_id (Union[None, UUID]): One act over several followers: a group's close, or a leader's retire; null for an
                unfollow
            cause (CopyCloseCause):
            reason (Union[None, str]): The retire's or the group close's reason as sent
            cutoff_at (Union[None, datetime.datetime]): Null: every copied position. A time: those opened by leader deals
                signalled at or before it
            requested_by (str): The API key's id, or the operator
            attempt (int):
            next_attempt_at (Union[None, datetime.datetime]): When MFX Hub looks at it again; null once it is not pending
            state (CopyCloseState): pending: still being closed. done: every copied position closed or found closed.
                incomplete: any not closed. superseded: a newer request for the follower took over its open positions
            created_at (datetime.datetime):
            finished_at (Union[None, datetime.datetime]):
            entries (list['CopyCloseEntry']):
    """

    id: UUID
    follower_id: UUID
    leader_id: UUID
    account_id: UUID
    group_id: Union[None, UUID]
    batch_id: Union[None, UUID]
    cause: CopyCloseCause
    reason: Union[None, str]
    cutoff_at: Union[None, datetime.datetime]
    requested_by: str
    attempt: int
    next_attempt_at: Union[None, datetime.datetime]
    state: CopyCloseState
    created_at: datetime.datetime
    finished_at: Union[None, datetime.datetime]
    entries: list["CopyCloseEntry"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_close_entry import CopyCloseEntry

        id = str(self.id)

        follower_id = str(self.follower_id)

        leader_id = str(self.leader_id)

        account_id = str(self.account_id)

        group_id: Union[None, str]
        if isinstance(self.group_id, UUID):
            group_id = str(self.group_id)
        else:
            group_id = self.group_id

        batch_id: Union[None, str]
        if isinstance(self.batch_id, UUID):
            batch_id = str(self.batch_id)
        else:
            batch_id = self.batch_id

        cause = self.cause.value

        reason: Union[None, str]
        reason = self.reason

        cutoff_at: Union[None, str]
        if isinstance(self.cutoff_at, datetime.datetime):
            cutoff_at = self.cutoff_at.isoformat()
        else:
            cutoff_at = self.cutoff_at

        requested_by = self.requested_by

        attempt = self.attempt

        next_attempt_at: Union[None, str]
        if isinstance(self.next_attempt_at, datetime.datetime):
            next_attempt_at = self.next_attempt_at.isoformat()
        else:
            next_attempt_at = self.next_attempt_at

        state = self.state.value

        created_at = self.created_at.isoformat()

        finished_at: Union[None, str]
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "follower_id": follower_id,
                "leader_id": leader_id,
                "account_id": account_id,
                "group_id": group_id,
                "batch_id": batch_id,
                "cause": cause,
                "reason": reason,
                "cutoff_at": cutoff_at,
                "requested_by": requested_by,
                "attempt": attempt,
                "next_attempt_at": next_attempt_at,
                "state": state,
                "created_at": created_at,
                "finished_at": finished_at,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_close_entry import CopyCloseEntry

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        follower_id = UUID(d.pop("follower_id"))

        leader_id = UUID(d.pop("leader_id"))

        account_id = UUID(d.pop("account_id"))

        def _parse_group_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_id_type_0 = UUID(data)

                return group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        group_id = _parse_group_id(d.pop("group_id"))

        def _parse_batch_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                batch_id_type_0 = UUID(data)

                return batch_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        batch_id = _parse_batch_id(d.pop("batch_id"))

        cause = CopyCloseCause._read(d.pop("cause"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_cutoff_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cutoff_at_type_0 = isoparse(data)

                return cutoff_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        cutoff_at = _parse_cutoff_at(d.pop("cutoff_at"))

        requested_by = d.pop("requested_by")

        attempt = d.pop("attempt")

        def _parse_next_attempt_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_attempt_at_type_0 = isoparse(data)

                return next_attempt_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_attempt_at = _parse_next_attempt_at(d.pop("next_attempt_at"))

        state = CopyCloseState._read(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_finished_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = CopyCloseEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        copy_close = cls(
            id=id,
            follower_id=follower_id,
            leader_id=leader_id,
            account_id=account_id,
            group_id=group_id,
            batch_id=batch_id,
            cause=cause,
            reason=reason,
            cutoff_at=cutoff_at,
            requested_by=requested_by,
            attempt=attempt,
            next_attempt_at=next_attempt_at,
            state=state,
            created_at=created_at,
            finished_at=finished_at,
            entries=entries,
        )

        copy_close.additional_properties = d
        return copy_close

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
