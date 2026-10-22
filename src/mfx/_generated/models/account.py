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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_profile_type_0 import AccountProfileType0
    from ..models.account_snapshot_type_0 import AccountSnapshotType0


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """What the terminal's account looks like now: the fast numerics and the slow facts. The cell reads the account every
    250 ms while positions are open and sends it when it changes (every 60 s flat); this answers from the platform's
    latest copy, never a round trip to the cell, and the same numbers are pushed on the stream's `account:{terminal_id}`
    channel as an `account.snapshot`, then `account.marks` (not on `events`). Each half carries when it was observed; a
    half never observed is null, not zero.

        Attributes:
            terminal_id (UUID):
            stale (bool): True when nothing arrived from the cell for 15 s with positions open (three missed keep-alives) or
                180 s flat; the numbers are then the last known, as of `snapshot.ts`
            snapshot (Union['AccountSnapshotType0', None]):
            profile (Union['AccountProfileType0', None]):
    """

    terminal_id: UUID
    stale: bool
    snapshot: Union["AccountSnapshotType0", None]
    profile: Union["AccountProfileType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_profile_type_0 import AccountProfileType0
        from ..models.account_snapshot_type_0 import AccountSnapshotType0

        terminal_id = str(self.terminal_id)

        stale = self.stale

        snapshot: Union[None, dict[str, Any]]
        if isinstance(self.snapshot, AccountSnapshotType0):
            snapshot = self.snapshot.to_dict()
        else:
            snapshot = self.snapshot

        profile: Union[None, dict[str, Any]]
        if isinstance(self.profile, AccountProfileType0):
            profile = self.profile.to_dict()
        else:
            profile = self.profile

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "stale": stale,
                "snapshot": snapshot,
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_profile_type_0 import AccountProfileType0
        from ..models.account_snapshot_type_0 import AccountSnapshotType0

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        stale = d.pop("stale")

        def _parse_snapshot(data: object) -> Union["AccountSnapshotType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                snapshot_type_0 = AccountSnapshotType0.from_dict(data)

                return snapshot_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AccountSnapshotType0", None], data)

        snapshot = _parse_snapshot(d.pop("snapshot"))

        def _parse_profile(data: object) -> Union["AccountProfileType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                profile_type_0 = AccountProfileType0.from_dict(data)

                return profile_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AccountProfileType0", None], data)

        profile = _parse_profile(d.pop("profile"))

        account = cls(
            terminal_id=terminal_id,
            stale=stale,
            snapshot=snapshot,
            profile=profile,
        )

        account.additional_properties = d
        return account

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
