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

from ..models.trading_account_runners_item_role_type_1 import (
    TradingAccountRunnersItemRoleType1,
)
from ..models.trading_account_runners_item_role_type_2_type_1 import (
    TradingAccountRunnersItemRoleType2Type1,
)
from ..models.trading_account_runners_item_role_type_3_type_1 import (
    TradingAccountRunnersItemRoleType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TradingAccountRunnersItem")


@_attrs_define
class TradingAccountRunnersItem:
    """
    Attributes:
        terminal_id (UUID):
        role (Union[None, TradingAccountRunnersItemRoleType1, TradingAccountRunnersItemRoleType2Type1,
            TradingAccountRunnersItemRoleType3Type1]): With HA, which terminal places orders; null without HA
    """

    terminal_id: UUID
    role: Union[
        None,
        TradingAccountRunnersItemRoleType1,
        TradingAccountRunnersItemRoleType2Type1,
        TradingAccountRunnersItemRoleType3Type1,
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_id = str(self.terminal_id)

        role: Union[None, str]
        if isinstance(self.role, TradingAccountRunnersItemRoleType1):
            role = self.role.value
        elif isinstance(self.role, TradingAccountRunnersItemRoleType2Type1):
            role = self.role.value
        elif isinstance(self.role, TradingAccountRunnersItemRoleType3Type1):
            role = self.role.value
        else:
            role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        def _parse_role(
            data: object,
        ) -> Union[
            None,
            TradingAccountRunnersItemRoleType1,
            TradingAccountRunnersItemRoleType2Type1,
            TradingAccountRunnersItemRoleType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_1 = TradingAccountRunnersItemRoleType1(data)

                return role_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_2_type_1 = TradingAccountRunnersItemRoleType2Type1(data)

                return role_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_3_type_1 = TradingAccountRunnersItemRoleType3Type1(data)

                return role_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TradingAccountRunnersItemRoleType1,
                    TradingAccountRunnersItemRoleType2Type1,
                    TradingAccountRunnersItemRoleType3Type1,
                ],
                data,
            )

        role = _parse_role(d.pop("role"))

        trading_account_runners_item = cls(
            terminal_id=terminal_id,
            role=role,
        )

        trading_account_runners_item.additional_properties = d
        return trading_account_runners_item

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
