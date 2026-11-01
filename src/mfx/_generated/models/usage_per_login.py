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
    from ..models.usage_per_login_servers_item import UsagePerLoginServersItem


T = TypeVar("T", bound="UsagePerLogin")


@_attrs_define
class UsagePerLogin:
    """How many terminals may run on one broker login.

    Attributes:
        plan_limit (int): 0: only the broker server's own limit applies
        servers (list['UsagePerLoginServersItem']): Each enabled broker server, with the number of sessions it is known
            to allow on one login.
    """

    plan_limit: int
    servers: list["UsagePerLoginServersItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_per_login_servers_item import UsagePerLoginServersItem

        plan_limit = self.plan_limit

        servers = []
        for servers_item_data in self.servers:
            servers_item = servers_item_data.to_dict()
            servers.append(servers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_limit": plan_limit,
                "servers": servers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_per_login_servers_item import UsagePerLoginServersItem

        d = dict(src_dict)
        plan_limit = d.pop("plan_limit")

        servers = []
        _servers = d.pop("servers")
        for servers_item_data in _servers:
            servers_item = UsagePerLoginServersItem.from_dict(servers_item_data)

            servers.append(servers_item)

        usage_per_login = cls(
            plan_limit=plan_limit,
            servers=servers,
        )

        usage_per_login.additional_properties = d
        return usage_per_login

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
