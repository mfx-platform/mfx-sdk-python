from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_limit import UsageLimit


T = TypeVar("T", bound="UsageKey")


@_attrs_define
class UsageKey:
    """The limits as they apply to the calling key. For commands_per_s, commands_burst and ws_conns that is the tenant's
    ceiling, lowered by the key's own cap where it has one.

        Attributes:
            key_id (str):
            commands_per_s (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies
                it yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
                under `tenant` the ceiling for all the tenant's keys together.
            commands_burst (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies
                it yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
                under `tenant` the ceiling for all the tenant's keys together.
            md_msgs_per_s (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies it
                yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
                under `tenant` the ceiling for all the tenant's keys together.
            ws_conns (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies it yet,
                and how much of it is in use where that is measured. Under `key` it is the figure for the calling key; under
                `tenant` the ceiling for all the tenant's keys together.
            account_channels_per_conn (UsageLimit): One limit: the figure in force, where it comes from, whether the
                platform applies it yet, and how much of it is in use where that is measured. Under `key` it is the figure for
                the calling key; under `tenant` the ceiling for all the tenant's keys together.
    """

    key_id: str
    commands_per_s: "UsageLimit"
    commands_burst: "UsageLimit"
    md_msgs_per_s: "UsageLimit"
    ws_conns: "UsageLimit"
    account_channels_per_conn: "UsageLimit"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_limit import UsageLimit

        key_id = self.key_id

        commands_per_s = self.commands_per_s.to_dict()

        commands_burst = self.commands_burst.to_dict()

        md_msgs_per_s = self.md_msgs_per_s.to_dict()

        ws_conns = self.ws_conns.to_dict()

        account_channels_per_conn = self.account_channels_per_conn.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key_id": key_id,
                "commands_per_s": commands_per_s,
                "commands_burst": commands_burst,
                "md_msgs_per_s": md_msgs_per_s,
                "ws_conns": ws_conns,
                "account_channels_per_conn": account_channels_per_conn,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_limit import UsageLimit

        d = dict(src_dict)
        key_id = d.pop("key_id")

        commands_per_s = UsageLimit.from_dict(d.pop("commands_per_s"))

        commands_burst = UsageLimit.from_dict(d.pop("commands_burst"))

        md_msgs_per_s = UsageLimit.from_dict(d.pop("md_msgs_per_s"))

        ws_conns = UsageLimit.from_dict(d.pop("ws_conns"))

        account_channels_per_conn = UsageLimit.from_dict(d.pop("account_channels_per_conn"))

        usage_key = cls(
            key_id=key_id,
            commands_per_s=commands_per_s,
            commands_burst=commands_burst,
            md_msgs_per_s=md_msgs_per_s,
            ws_conns=ws_conns,
            account_channels_per_conn=account_channels_per_conn,
        )

        usage_key.additional_properties = d
        return usage_key

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
