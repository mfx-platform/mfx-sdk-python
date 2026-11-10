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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CtraderGrantAccount")


@_attrs_define
class CtraderGrantAccount:
    """One cTrader account the trader shared in this grant.

    Attributes:
        ctid_trader_account_id (str): cTrader's own id of the account
        live (bool):
        broker_name (Union[None, str]):
        login_masked (Union[None, str]): e.g. ****3456
        account_id (Union[None, UUID]): The MFX Hub account made from it, once chosen; null until then
    """

    ctid_trader_account_id: str
    live: bool
    broker_name: Union[None, str]
    login_masked: Union[None, str]
    account_id: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ctid_trader_account_id = self.ctid_trader_account_id

        live = self.live

        broker_name: Union[None, str]
        broker_name = self.broker_name

        login_masked: Union[None, str]
        login_masked = self.login_masked

        account_id: Union[None, str]
        if isinstance(self.account_id, UUID):
            account_id = str(self.account_id)
        else:
            account_id = self.account_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ctid_trader_account_id": ctid_trader_account_id,
                "live": live,
                "broker_name": broker_name,
                "login_masked": login_masked,
                "account_id": account_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ctid_trader_account_id = d.pop("ctid_trader_account_id")

        live = d.pop("live")

        def _parse_broker_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        broker_name = _parse_broker_name(d.pop("broker_name"))

        def _parse_login_masked(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        login_masked = _parse_login_masked(d.pop("login_masked"))

        def _parse_account_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                account_id_type_0 = UUID(data)

                return account_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        account_id = _parse_account_id(d.pop("account_id"))

        ctrader_grant_account = cls(
            ctid_trader_account_id=ctid_trader_account_id,
            live=live,
            broker_name=broker_name,
            login_masked=login_masked,
            account_id=account_id,
        )

        ctrader_grant_account.additional_properties = d
        return ctrader_grant_account

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
