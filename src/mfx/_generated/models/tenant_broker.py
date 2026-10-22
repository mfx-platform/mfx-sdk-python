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
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tenant_broker_status import TenantBrokerStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantBroker")


@_attrs_define
class TenantBroker:
    """
    Attributes:
        id (UUID):
        code (str):
        display_name (str):
        status (TenantBrokerStatus):
        symbol_suffix (Union[Unset, str]): The symbol variant this broker's accounts use by default; empty for plain
            names
    """

    id: UUID
    code: str
    display_name: str
    status: TenantBrokerStatus
    symbol_suffix: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        code = self.code

        display_name = self.display_name

        status = self.status.value

        symbol_suffix = self.symbol_suffix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "code": code,
                "display_name": display_name,
                "status": status,
            }
        )
        if symbol_suffix is not UNSET:
            field_dict["symbol_suffix"] = symbol_suffix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        code = d.pop("code")

        display_name = d.pop("display_name")

        status = TenantBrokerStatus(d.pop("status"))

        symbol_suffix = d.pop("symbol_suffix", UNSET)

        tenant_broker = cls(
            id=id,
            code=code,
            display_name=display_name,
            status=status,
            symbol_suffix=symbol_suffix,
        )

        tenant_broker.additional_properties = d
        return tenant_broker

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
