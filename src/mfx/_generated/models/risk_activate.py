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

T = TypeVar("T", bound="RiskActivate")


@_attrs_define
class RiskActivate:
    """
    Attributes:
        account_ids (list[UUID]):
        version (int):
        reason (Union[None, Unset, str]): Needed for an account where the version relaxes the one in force
    """

    account_ids: list[UUID]
    version: int
    reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_ids = []
        for account_ids_item_data in self.account_ids:
            account_ids_item = str(account_ids_item_data)
            account_ids.append(account_ids_item)

        version = self.version

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_ids": account_ids,
                "version": version,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_ids = []
        _account_ids = d.pop("account_ids")
        for account_ids_item_data in _account_ids:
            account_ids_item = UUID(account_ids_item_data)

            account_ids.append(account_ids_item)

        version = d.pop("version")

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        risk_activate = cls(
            account_ids=account_ids,
            version=version,
            reason=reason,
        )

        risk_activate.additional_properties = d
        return risk_activate

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
