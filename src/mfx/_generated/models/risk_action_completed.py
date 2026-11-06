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

from ..models.risk_action_completed_kind import RiskActionCompletedKind
from ..models.risk_action_completed_state import RiskActionCompletedState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_action_completed_accounts_item import (
        RiskActionCompletedAccountsItem,
    )
    from ..models.risk_action_completed_unresolved_item import (
        RiskActionCompletedUnresolvedItem,
    )


T = TypeVar("T", bound="RiskActionCompleted")


@_attrs_define
class RiskActionCompleted:
    """`data` of `risk.action_completed`: sent at each change of an action, with every account's and item's outcome

    Attributes:
        schema_version (str):
        action_id (UUID):
        kind (RiskActionCompletedKind):
        state (RiskActionCompletedState):
        accounts (list['RiskActionCompletedAccountsItem']):
        unresolved (list['RiskActionCompletedUnresolvedItem']):
        at (datetime.datetime):
    """

    schema_version: str
    action_id: UUID
    kind: RiskActionCompletedKind
    state: RiskActionCompletedState
    accounts: list["RiskActionCompletedAccountsItem"]
    unresolved: list["RiskActionCompletedUnresolvedItem"]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_action_completed_accounts_item import (
            RiskActionCompletedAccountsItem,
        )
        from ..models.risk_action_completed_unresolved_item import (
            RiskActionCompletedUnresolvedItem,
        )

        schema_version = self.schema_version

        action_id = str(self.action_id)

        kind = self.kind.value

        state = self.state.value

        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        unresolved = []
        for unresolved_item_data in self.unresolved:
            unresolved_item = unresolved_item_data.to_dict()
            unresolved.append(unresolved_item)

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "action_id": action_id,
                "kind": kind,
                "state": state,
                "accounts": accounts,
                "unresolved": unresolved,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_action_completed_accounts_item import (
            RiskActionCompletedAccountsItem,
        )
        from ..models.risk_action_completed_unresolved_item import (
            RiskActionCompletedUnresolvedItem,
        )

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        action_id = UUID(d.pop("action_id"))

        kind = RiskActionCompletedKind(d.pop("kind"))

        state = RiskActionCompletedState(d.pop("state"))

        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = RiskActionCompletedAccountsItem.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        unresolved = []
        _unresolved = d.pop("unresolved")
        for unresolved_item_data in _unresolved:
            unresolved_item = RiskActionCompletedUnresolvedItem.from_dict(unresolved_item_data)

            unresolved.append(unresolved_item)

        at = isoparse(d.pop("at"))

        risk_action_completed = cls(
            schema_version=schema_version,
            action_id=action_id,
            kind=kind,
            state=state,
            accounts=accounts,
            unresolved=unresolved,
            at=at,
        )

        risk_action_completed.additional_properties = d
        return risk_action_completed

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
