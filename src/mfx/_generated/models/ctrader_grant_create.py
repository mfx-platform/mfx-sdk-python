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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ctrader_grant_create_environment import CtraderGrantCreateEnvironment
from ..models.ctrader_grant_create_scope import CtraderGrantCreateScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="CtraderGrantCreate")


@_attrs_define
class CtraderGrantCreate:
    """Start connecting a trader's cTrader accounts. Send the trader to `consent_url`: they sign in at cTrader, choose the
    accounts to share, and come back to `return_url`.

        Attributes:
            environment (CtraderGrantCreateEnvironment): live or demo accounts; one grant covers one of them
            scope (CtraderGrantCreateScope): accounts: read the accounts only; trading: read them and place orders on them
            return_url (str): Where the trader is sent after consent, https only. MFX Hub adds `grant_id`, `result`
                (`granted`, `denied` or `failed`) and your `tenant_state` as query parameters.
            tenant_state (Union[None, Unset, str]): Your own value, returned unchanged on return_url; never read by MFX Hub
    """

    environment: CtraderGrantCreateEnvironment
    scope: CtraderGrantCreateScope
    return_url: str
    tenant_state: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        environment = self.environment.value

        scope = self.scope.value

        return_url = self.return_url

        tenant_state: Union[None, Unset, str]
        if isinstance(self.tenant_state, Unset):
            tenant_state = UNSET
        else:
            tenant_state = self.tenant_state

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "environment": environment,
                "scope": scope,
                "return_url": return_url,
            }
        )
        if tenant_state is not UNSET:
            field_dict["tenant_state"] = tenant_state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        environment = CtraderGrantCreateEnvironment(d.pop("environment"))

        scope = CtraderGrantCreateScope(d.pop("scope"))

        return_url = d.pop("return_url")

        def _parse_tenant_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tenant_state = _parse_tenant_state(d.pop("tenant_state", UNSET))

        ctrader_grant_create = cls(
            environment=environment,
            scope=scope,
            return_url=return_url,
            tenant_state=tenant_state,
        )

        return ctrader_grant_create
