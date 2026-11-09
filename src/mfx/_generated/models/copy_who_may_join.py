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

from ..models.copy_who_may_join_accounts import CopyWhoMayJoinAccounts
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyWhoMayJoin")


@_attrs_define
class CopyWhoMayJoin:
    """Which of your accounts may follow this leader

    Attributes:
        accounts (Union[Unset, CopyWhoMayJoinAccounts]): any: any of your accounts. listed: only those in account_ids
            Default: CopyWhoMayJoinAccounts.ANY.
        account_ids (Union[Unset, list[UUID]]):
    """

    accounts: Union[Unset, CopyWhoMayJoinAccounts] = CopyWhoMayJoinAccounts.ANY
    account_ids: Union[Unset, list[UUID]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        accounts: Union[Unset, str] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.value

        account_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.account_ids, Unset):
            account_ids = []
            for account_ids_item_data in self.account_ids:
                account_ids_item = str(account_ids_item_data)
                account_ids.append(account_ids_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if account_ids is not UNSET:
            field_dict["account_ids"] = account_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _accounts = d.pop("accounts", UNSET)
        accounts: Union[Unset, CopyWhoMayJoinAccounts]
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = CopyWhoMayJoinAccounts(_accounts)

        account_ids = []
        _account_ids = d.pop("account_ids", UNSET)
        for account_ids_item_data in _account_ids or []:
            account_ids_item = UUID(account_ids_item_data)

            account_ids.append(account_ids_item)

        copy_who_may_join = cls(
            accounts=accounts,
            account_ids=account_ids,
        )

        return copy_who_may_join
