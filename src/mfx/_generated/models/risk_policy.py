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
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.risk_policy_state import RiskPolicyState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_policy_accounts_item import RiskPolicyAccountsItem
    from ..models.risk_policy_version import RiskPolicyVersion


T = TypeVar("T", bound="RiskPolicy")


@_attrs_define
class RiskPolicy:
    """
    Attributes:
        id (UUID):
        name (str):
        state (RiskPolicyState):
        current_version (RiskPolicyVersion):
        accounts (list['RiskPolicyAccountsItem']):
        created_at (datetime.datetime):
    """

    id: UUID
    name: str
    state: RiskPolicyState
    current_version: "RiskPolicyVersion"
    accounts: list["RiskPolicyAccountsItem"]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_policy_accounts_item import RiskPolicyAccountsItem
        from ..models.risk_policy_version import RiskPolicyVersion

        id = str(self.id)

        name = self.name

        state = self.state.value

        current_version = self.current_version.to_dict()

        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "state": state,
                "current_version": current_version,
                "accounts": accounts,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_policy_accounts_item import RiskPolicyAccountsItem
        from ..models.risk_policy_version import RiskPolicyVersion

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        state = RiskPolicyState(d.pop("state"))

        current_version = RiskPolicyVersion.from_dict(d.pop("current_version"))

        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = RiskPolicyAccountsItem.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        created_at = isoparse(d.pop("created_at"))

        risk_policy = cls(
            id=id,
            name=name,
            state=state,
            current_version=current_version,
            accounts=accounts,
            created_at=created_at,
        )

        risk_policy.additional_properties = d
        return risk_policy

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
