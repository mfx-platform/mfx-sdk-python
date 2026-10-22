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
    from ..models.tenant_terminal_conditions_additional_property import (
        TenantTerminalConditionsAdditionalProperty,
    )


T = TypeVar("T", bound="TenantTerminalConditions")


@_attrs_define
class TenantTerminalConditions:
    """ProcessRunning, BrokerConnected, TicksFresh, TradeAllowed, CredentialLeased — each {status, reason, since,
    attributed_to}; absent means not yet observed

    """

    additional_properties: dict[str, "TenantTerminalConditionsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.tenant_terminal_conditions_additional_property import (
            TenantTerminalConditionsAdditionalProperty,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tenant_terminal_conditions_additional_property import (
            TenantTerminalConditionsAdditionalProperty,
        )

        d = dict(src_dict)
        tenant_terminal_conditions = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = TenantTerminalConditionsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        tenant_terminal_conditions.additional_properties = additional_properties
        return tenant_terminal_conditions

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "TenantTerminalConditionsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "TenantTerminalConditionsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
