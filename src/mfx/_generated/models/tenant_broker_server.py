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

from ..models.tenant_broker_server_kind import TenantBrokerServerKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantBrokerServer")


@_attrs_define
class TenantBrokerServer:
    """
    Attributes:
        id (UUID):
        server_name (str): The MT5 server string a credential is submitted for
        kind (TenantBrokerServerKind):
        enabled (bool): False: MFX does not use this server now. A terminal or credential for it is refused 409
            broker_not_supported (refused_by server_disabled); try another server of the same broker.
        disabled_reason (Union[None, str]): The sentence the operator recorded; null while enabled. The same words the
            refusal carries
    """

    id: UUID
    server_name: str
    kind: TenantBrokerServerKind
    enabled: bool
    disabled_reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        server_name = self.server_name

        kind = self.kind.value

        enabled = self.enabled

        disabled_reason: Union[None, str]
        disabled_reason = self.disabled_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "server_name": server_name,
                "kind": kind,
                "enabled": enabled,
                "disabled_reason": disabled_reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        server_name = d.pop("server_name")

        kind = TenantBrokerServerKind(d.pop("kind"))

        enabled = d.pop("enabled")

        def _parse_disabled_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        disabled_reason = _parse_disabled_reason(d.pop("disabled_reason"))

        tenant_broker_server = cls(
            id=id,
            server_name=server_name,
            kind=kind,
            enabled=enabled,
            disabled_reason=disabled_reason,
        )

        tenant_broker_server.additional_properties = d
        return tenant_broker_server

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
