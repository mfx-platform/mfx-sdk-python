from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.usage_tenant_terminals_source import UsageTenantTerminalsSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageTenantTerminals")


@_attrs_define
class UsageTenantTerminals:
    """Terminals the tenant may have, not counting retired ones. A request over it is 409 `quota_exceeded`.

    Attributes:
        limit (int):
        used (int):
        source (UsageTenantTerminalsSource):
    """

    limit: int
    used: int
    source: UsageTenantTerminalsSource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        used = self.used

        source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "used": used,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit")

        used = d.pop("used")

        source = UsageTenantTerminalsSource(d.pop("source"))

        usage_tenant_terminals = cls(
            limit=limit,
            used=used,
            source=source,
        )

        usage_tenant_terminals.additional_properties = d
        return usage_tenant_terminals

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
