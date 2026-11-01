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
    from ..models.usage_tenant_terminals import UsageTenantTerminals


T = TypeVar("T", bound="UsageTenant")


@_attrs_define
class UsageTenant:
    """
    Attributes:
        commands_per_s (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies
            it yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
            under `tenant` the ceiling for all the tenant's keys together.
        commands_burst (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies
            it yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
            under `tenant` the ceiling for all the tenant's keys together.
        ws_conns (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies it yet,
            and how much of it is in use where that is measured. Under `key` it is the figure for the calling key; under
            `tenant` the ceiling for all the tenant's keys together.
        terminals (UsageTenantTerminals): Terminals the tenant may have, not counting retired ones. A request over it is
            409 `quota_exceeded`.
    """

    commands_per_s: "UsageLimit"
    commands_burst: "UsageLimit"
    ws_conns: "UsageLimit"
    terminals: "UsageTenantTerminals"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_limit import UsageLimit
        from ..models.usage_tenant_terminals import UsageTenantTerminals

        commands_per_s = self.commands_per_s.to_dict()

        commands_burst = self.commands_burst.to_dict()

        ws_conns = self.ws_conns.to_dict()

        terminals = self.terminals.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commands_per_s": commands_per_s,
                "commands_burst": commands_burst,
                "ws_conns": ws_conns,
                "terminals": terminals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_limit import UsageLimit
        from ..models.usage_tenant_terminals import UsageTenantTerminals

        d = dict(src_dict)
        commands_per_s = UsageLimit.from_dict(d.pop("commands_per_s"))

        commands_burst = UsageLimit.from_dict(d.pop("commands_burst"))

        ws_conns = UsageLimit.from_dict(d.pop("ws_conns"))

        terminals = UsageTenantTerminals.from_dict(d.pop("terminals"))

        usage_tenant = cls(
            commands_per_s=commands_per_s,
            commands_burst=commands_burst,
            ws_conns=ws_conns,
            terminals=terminals,
        )

        usage_tenant.additional_properties = d
        return usage_tenant

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
