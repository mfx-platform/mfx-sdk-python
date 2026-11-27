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

from ..models.billing_price_list_plans_item_pay_type_1 import (
    BillingPriceListPlansItemPayType1,
)
from ..models.billing_price_list_plans_item_pay_type_2_type_1 import (
    BillingPriceListPlansItemPayType2Type1,
)
from ..models.billing_price_list_plans_item_pay_type_3_type_1 import (
    BillingPriceListPlansItemPayType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingPriceListPlansItem")


@_attrs_define
class BillingPriceListPlansItem:
    """
    Attributes:
        key (str):
        name (str):
        price (Union[None, Unset, str]): free, or contract; null when priced per item
        accounts (Union[None, Unset, str]):
        max_running_accounts (Union[None, Unset, int]):
        pay (Union[BillingPriceListPlansItemPayType1, BillingPriceListPlansItemPayType2Type1,
            BillingPriceListPlansItemPayType3Type1, None, Unset]):
        block_terminals (Union[None, Unset, int]):
        talk_to_sales (Union[Unset, bool]):
    """

    key: str
    name: str
    price: Union[None, Unset, str] = UNSET
    accounts: Union[None, Unset, str] = UNSET
    max_running_accounts: Union[None, Unset, int] = UNSET
    pay: Union[
        BillingPriceListPlansItemPayType1,
        BillingPriceListPlansItemPayType2Type1,
        BillingPriceListPlansItemPayType3Type1,
        None,
        Unset,
    ] = UNSET
    block_terminals: Union[None, Unset, int] = UNSET
    talk_to_sales: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        name = self.name

        price: Union[None, Unset, str]
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        accounts: Union[None, Unset, str]
        if isinstance(self.accounts, Unset):
            accounts = UNSET
        else:
            accounts = self.accounts

        max_running_accounts: Union[None, Unset, int]
        if isinstance(self.max_running_accounts, Unset):
            max_running_accounts = UNSET
        else:
            max_running_accounts = self.max_running_accounts

        pay: Union[None, Unset, str]
        if isinstance(self.pay, Unset):
            pay = UNSET
        elif isinstance(self.pay, BillingPriceListPlansItemPayType1):
            pay = self.pay.value
        elif isinstance(self.pay, BillingPriceListPlansItemPayType2Type1):
            pay = self.pay.value
        elif isinstance(self.pay, BillingPriceListPlansItemPayType3Type1):
            pay = self.pay.value
        else:
            pay = self.pay

        block_terminals: Union[None, Unset, int]
        if isinstance(self.block_terminals, Unset):
            block_terminals = UNSET
        else:
            block_terminals = self.block_terminals

        talk_to_sales = self.talk_to_sales

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "name": name,
            }
        )
        if price is not UNSET:
            field_dict["price"] = price
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if max_running_accounts is not UNSET:
            field_dict["max_running_accounts"] = max_running_accounts
        if pay is not UNSET:
            field_dict["pay"] = pay
        if block_terminals is not UNSET:
            field_dict["block_terminals"] = block_terminals
        if talk_to_sales is not UNSET:
            field_dict["talk_to_sales"] = talk_to_sales

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        name = d.pop("name")

        def _parse_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_accounts(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        accounts = _parse_accounts(d.pop("accounts", UNSET))

        def _parse_max_running_accounts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_running_accounts = _parse_max_running_accounts(d.pop("max_running_accounts", UNSET))

        def _parse_pay(
            data: object,
        ) -> Union[
            BillingPriceListPlansItemPayType1,
            BillingPriceListPlansItemPayType2Type1,
            BillingPriceListPlansItemPayType3Type1,
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pay_type_1 = BillingPriceListPlansItemPayType1._read(data)

                return pay_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pay_type_2_type_1 = BillingPriceListPlansItemPayType2Type1._read(data)

                return pay_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pay_type_3_type_1 = BillingPriceListPlansItemPayType3Type1._read(data)

                return pay_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    BillingPriceListPlansItemPayType1,
                    BillingPriceListPlansItemPayType2Type1,
                    BillingPriceListPlansItemPayType3Type1,
                    None,
                    Unset,
                ],
                data,
            )

        pay = _parse_pay(d.pop("pay", UNSET))

        def _parse_block_terminals(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        block_terminals = _parse_block_terminals(d.pop("block_terminals", UNSET))

        talk_to_sales = d.pop("talk_to_sales", UNSET)

        billing_price_list_plans_item = cls(
            key=key,
            name=name,
            price=price,
            accounts=accounts,
            max_running_accounts=max_running_accounts,
            pay=pay,
            block_terminals=block_terminals,
            talk_to_sales=talk_to_sales,
        )

        billing_price_list_plans_item.additional_properties = d
        return billing_price_list_plans_item

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
