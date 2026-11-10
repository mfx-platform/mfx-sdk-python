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
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.ctrader_grant_environment import CtraderGrantEnvironment
from ..models.ctrader_grant_scope import CtraderGrantScope
from ..models.ctrader_grant_state import CtraderGrantState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ctrader_grant_account import CtraderGrantAccount


T = TypeVar("T", bound="CtraderGrant")


@_attrs_define
class CtraderGrant:
    """
    Attributes:
        id (UUID):
        environment (CtraderGrantEnvironment):
        scope (CtraderGrantScope):
        state (CtraderGrantState): PENDING: waiting for the trader's consent. ACTIVE: granted; its accounts are listed.
            REVOKED: you revoked it, or the trader withdrew it at cTrader. EXPIRED: the consent was not completed in time.
        return_url (Union[None, str]):
        tenant_state (Union[None, str]):
        created_at (datetime.datetime):
        granted_at (Union[None, datetime.datetime]):
        revoked_at (Union[None, datetime.datetime]):
        accounts (list['CtraderGrantAccount']): Empty until the grant is ACTIVE
    """

    id: UUID
    environment: CtraderGrantEnvironment
    scope: CtraderGrantScope
    state: CtraderGrantState
    return_url: Union[None, str]
    tenant_state: Union[None, str]
    created_at: datetime.datetime
    granted_at: Union[None, datetime.datetime]
    revoked_at: Union[None, datetime.datetime]
    accounts: list["CtraderGrantAccount"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ctrader_grant_account import CtraderGrantAccount

        id = str(self.id)

        environment = self.environment.value

        scope = self.scope.value

        state = self.state.value

        return_url: Union[None, str]
        return_url = self.return_url

        tenant_state: Union[None, str]
        tenant_state = self.tenant_state

        created_at = self.created_at.isoformat()

        granted_at: Union[None, str]
        if isinstance(self.granted_at, datetime.datetime):
            granted_at = self.granted_at.isoformat()
        else:
            granted_at = self.granted_at

        revoked_at: Union[None, str]
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "environment": environment,
                "scope": scope,
                "state": state,
                "return_url": return_url,
                "tenant_state": tenant_state,
                "created_at": created_at,
                "granted_at": granted_at,
                "revoked_at": revoked_at,
                "accounts": accounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ctrader_grant_account import CtraderGrantAccount

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        environment = CtraderGrantEnvironment(d.pop("environment"))

        scope = CtraderGrantScope(d.pop("scope"))

        state = CtraderGrantState(d.pop("state"))

        def _parse_return_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        return_url = _parse_return_url(d.pop("return_url"))

        def _parse_tenant_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tenant_state = _parse_tenant_state(d.pop("tenant_state"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_granted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                granted_at_type_0 = isoparse(data)

                return granted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        granted_at = _parse_granted_at(d.pop("granted_at"))

        def _parse_revoked_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at"))

        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = CtraderGrantAccount.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        ctrader_grant = cls(
            id=id,
            environment=environment,
            scope=scope,
            state=state,
            return_url=return_url,
            tenant_state=tenant_state,
            created_at=created_at,
            granted_at=granted_at,
            revoked_at=revoked_at,
            accounts=accounts,
        )

        ctrader_grant.additional_properties = d
        return ctrader_grant

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
