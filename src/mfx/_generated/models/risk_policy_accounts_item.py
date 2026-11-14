from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.risk_policy_accounts_item_state import RiskPolicyAccountsItemState
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPolicyAccountsItem")


@_attrs_define
class RiskPolicyAccountsItem:
    """
    Attributes:
        account_id (UUID):
        version (int):
        state (RiskPolicyAccountsItemState):
    """

    account_id: UUID
    version: int
    state: RiskPolicyAccountsItemState
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = str(self.account_id)

        version = self.version

        state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "version": version,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        version = d.pop("version")

        state = RiskPolicyAccountsItemState(d.pop("state"))

        risk_policy_accounts_item = cls(
            account_id=account_id,
            version=version,
            state=state,
        )

        risk_policy_accounts_item.additional_properties = d
        return risk_policy_accounts_item

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
