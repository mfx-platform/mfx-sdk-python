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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_price_list_currency import BillingPriceListCurrency
from ..models.billing_price_list_scope import BillingPriceListScope
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_agreement_ref import BillingAgreementRef
    from ..models.billing_price_list_accounts_type_0 import BillingPriceListAccountsType0
    from ..models.billing_price_list_items_item import BillingPriceListItemsItem
    from ..models.billing_price_list_next_type_0 import BillingPriceListNextType0
    from ..models.billing_price_list_plans_item import BillingPriceListPlansItem
    from ..models.billing_price_list_talk_to_sales_when_type_0 import (
        BillingPriceListTalkToSalesWhenType0,
    )


T = TypeVar("T", bound="BillingPriceList")


@_attrs_define
class BillingPriceList:
    """A price list: the plans and every item with its monthly price. Billing is per day: each account and each add-on on
    it costs its monthly price divided by the days in that month, for every day it exists, with a minimum of one day; a
    full month costs the monthly price.

        Example:
            {'version': 'rc_v3', 'scope': 'list', 'effective_from': '2026-12-01T00:00:00Z', 'currency': 'USD', 'rule': 'Per
                account, and per add-on on it, for every day it exists: the monthly price divided by the days in that month, at
                least one day. A full month is the monthly price.', 'plans': [{'key': 'developer', 'name': 'Developer', 'price':
                'free', 'accounts': '1 demo account, 30 days'}, {'key': 'standard', 'name': 'Standard', 'max_running_accounts':
                50, 'pay': 'prepaid_card'}, {'key': 'enterprise', 'name': 'Enterprise', 'price': 'contract', 'block_terminals':
                20, 'pay': 'invoice_or_prepaid', 'talk_to_sales': True}], 'items': [{'key': 'account.mt5', 'kind': 'base',
                'venue': 'mt5', 'name': 'MetaTrader 5® account', 'unit': 'account_month', 'monthly_usd': '7.50', 'plans':
                {'standard': 'available', 'enterprise': 'contract'}}, {'key': 'account.ctrader', 'kind': 'base', 'venue':
                'ctrader', 'name': 'cTrader account', 'unit': 'account_month', 'monthly_usd': '2.50', 'plans': {'standard':
                'available', 'enterprise': 'contract'}}, {'key': 'addon.expert_advisors', 'kind': 'add_on', 'venue': 'mt5',
                'name': 'Expert advisors', 'unit': 'account_month', 'monthly_usd': '6.00', 'plans': {'standard': 'available',
                'enterprise': 'contract'}}, {'key': 'addon.copy_follower', 'kind': 'add_on', 'name': 'Copy Trading (follower)',
                'unit': 'account_month', 'monthly_usd': '1.00', 'plans': {'standard': 'available', 'enterprise': 'contract'}},
                {'key': 'addon.risk_management', 'kind': 'add_on', 'name': 'Risk Management', 'unit': 'account_month',
                'monthly_usd': '2.00', 'plans': {'standard': 'available', 'enterprise': 'contract'}}, {'key':
                'addon.trading_statistics', 'kind': 'add_on', 'name': 'Trading statistics', 'unit': 'account_month',
                'monthly_usd': '0.00', 'plans': {'standard': 'included', 'enterprise': 'included'}}, {'key': 'enterprise.block',
                'kind': 'block', 'venue': 'mt5', 'name': 'Enterprise block (20 terminals)', 'unit': 'block_month',
                'monthly_usd': '210.00', 'includes': ['account.mt5', 'addon.copy_follower', 'addon.risk_management'],
                'provisional': 'until the confidential cells are measured', 'plans': {'standard': 'none', 'enterprise':
                'minimum_one'}}], 'included': ['API and SDKs', 'the stream', 'webhooks', 'market data for your accounts',
                'history', 'trading statistics', 'refresh every 1000 ms'], 'talk_to_sales_when': {'running_accounts_over': 50,
                'estimate_usd_over': '500.00', 'items': ['addon.ha_active_active', 'enterprise.block']}, 'next': {'version':
                'rc_v4', 'effective_from': '2027-01-01T00:00:00Z', 'changes': [{'key': 'account.mt5', 'monthly_usd': '8.00'}]},
                'as_of': '2026-11-16T12:00:00Z'}

        Attributes:
            version (str):
            effective_from (datetime.datetime):
            currency (BillingPriceListCurrency):
            rule (str): The billing rule in one sentence
            plans (list['BillingPriceListPlansItem']):
            items (list['BillingPriceListItemsItem']):
            scope (Union[Unset, BillingPriceListScope]): tenant: your agreement's own prices (GET /billing/prices only)
            agreement (Union['BillingAgreementRef', None, Unset]): Your own prices only: the agreement they come from; null
                or absent on the list
            included (Union[Unset, list[str]]):
            talk_to_sales_when (Union['BillingPriceListTalkToSalesWhenType0', None, Unset]):
            next_ (Union['BillingPriceListNextType0', None, Unset]): The next list version once it is released, with the
                date it starts and what changes
            as_of (Union[Unset, datetime.datetime]):
            accounts (Union['BillingPriceListAccountsType0', None, Unset]): Your own prices only (GET /billing/prices): the
                accounts the Standard prices tile reads. Absent from the public list
    """

    version: str
    effective_from: datetime.datetime
    currency: BillingPriceListCurrency
    rule: str
    plans: list["BillingPriceListPlansItem"]
    items: list["BillingPriceListItemsItem"]
    scope: Union[Unset, BillingPriceListScope] = UNSET
    agreement: Union["BillingAgreementRef", None, Unset] = UNSET
    included: Union[Unset, list[str]] = UNSET
    talk_to_sales_when: Union["BillingPriceListTalkToSalesWhenType0", None, Unset] = UNSET
    next_: Union["BillingPriceListNextType0", None, Unset] = UNSET
    as_of: Union[Unset, datetime.datetime] = UNSET
    accounts: Union["BillingPriceListAccountsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_agreement_ref import BillingAgreementRef
        from ..models.billing_price_list_accounts_type_0 import (
            BillingPriceListAccountsType0,
        )
        from ..models.billing_price_list_items_item import BillingPriceListItemsItem
        from ..models.billing_price_list_next_type_0 import BillingPriceListNextType0
        from ..models.billing_price_list_plans_item import BillingPriceListPlansItem
        from ..models.billing_price_list_talk_to_sales_when_type_0 import (
            BillingPriceListTalkToSalesWhenType0,
        )

        version = self.version

        effective_from = self.effective_from.isoformat()

        currency = self.currency.value

        rule = self.rule

        plans = []
        for plans_item_data in self.plans:
            plans_item = plans_item_data.to_dict()
            plans.append(plans_item)

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        scope: Union[Unset, str] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        agreement: Union[None, Unset, dict[str, Any]]
        if isinstance(self.agreement, Unset):
            agreement = UNSET
        elif isinstance(self.agreement, BillingAgreementRef):
            agreement = self.agreement.to_dict()
        else:
            agreement = self.agreement

        included: Union[Unset, list[str]] = UNSET
        if not isinstance(self.included, Unset):
            included = self.included

        talk_to_sales_when: Union[None, Unset, dict[str, Any]]
        if isinstance(self.talk_to_sales_when, Unset):
            talk_to_sales_when = UNSET
        elif isinstance(self.talk_to_sales_when, BillingPriceListTalkToSalesWhenType0):
            talk_to_sales_when = self.talk_to_sales_when.to_dict()
        else:
            talk_to_sales_when = self.talk_to_sales_when

        next_: Union[None, Unset, dict[str, Any]]
        if isinstance(self.next_, Unset):
            next_ = UNSET
        elif isinstance(self.next_, BillingPriceListNextType0):
            next_ = self.next_.to_dict()
        else:
            next_ = self.next_

        as_of: Union[Unset, str] = UNSET
        if not isinstance(self.as_of, Unset):
            as_of = self.as_of.isoformat()

        accounts: Union[None, Unset, dict[str, Any]]
        if isinstance(self.accounts, Unset):
            accounts = UNSET
        elif isinstance(self.accounts, BillingPriceListAccountsType0):
            accounts = self.accounts.to_dict()
        else:
            accounts = self.accounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "effective_from": effective_from,
                "currency": currency,
                "rule": rule,
                "plans": plans,
                "items": items,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope
        if agreement is not UNSET:
            field_dict["agreement"] = agreement
        if included is not UNSET:
            field_dict["included"] = included
        if talk_to_sales_when is not UNSET:
            field_dict["talk_to_sales_when"] = talk_to_sales_when
        if next_ is not UNSET:
            field_dict["next"] = next_
        if as_of is not UNSET:
            field_dict["as_of"] = as_of
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_agreement_ref import BillingAgreementRef
        from ..models.billing_price_list_accounts_type_0 import (
            BillingPriceListAccountsType0,
        )
        from ..models.billing_price_list_items_item import BillingPriceListItemsItem
        from ..models.billing_price_list_next_type_0 import BillingPriceListNextType0
        from ..models.billing_price_list_plans_item import BillingPriceListPlansItem
        from ..models.billing_price_list_talk_to_sales_when_type_0 import (
            BillingPriceListTalkToSalesWhenType0,
        )

        d = dict(src_dict)
        version = d.pop("version")

        effective_from = isoparse(d.pop("effective_from"))

        currency = BillingPriceListCurrency._read(d.pop("currency"))

        rule = d.pop("rule")

        plans = []
        _plans = d.pop("plans")
        for plans_item_data in _plans:
            plans_item = BillingPriceListPlansItem.from_dict(plans_item_data)

            plans.append(plans_item)

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = BillingPriceListItemsItem.from_dict(items_item_data)

            items.append(items_item)

        _scope = d.pop("scope", UNSET)
        scope: Union[Unset, BillingPriceListScope]
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = BillingPriceListScope._read(_scope)

        def _parse_agreement(data: object) -> Union["BillingAgreementRef", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agreement_type_0 = BillingAgreementRef.from_dict(data)

                return agreement_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingAgreementRef", None, Unset], data)

        agreement = _parse_agreement(d.pop("agreement", UNSET))

        included = cast(list[str], d.pop("included", UNSET))

        def _parse_talk_to_sales_when(
            data: object,
        ) -> Union["BillingPriceListTalkToSalesWhenType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                talk_to_sales_when_type_0 = BillingPriceListTalkToSalesWhenType0.from_dict(data)

                return talk_to_sales_when_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingPriceListTalkToSalesWhenType0", None, Unset], data)

        talk_to_sales_when = _parse_talk_to_sales_when(d.pop("talk_to_sales_when", UNSET))

        def _parse_next_(data: object) -> Union["BillingPriceListNextType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                next_type_0 = BillingPriceListNextType0.from_dict(data)

                return next_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingPriceListNextType0", None, Unset], data)

        next_ = _parse_next_(d.pop("next", UNSET))

        _as_of = d.pop("as_of", UNSET)
        as_of: Union[Unset, datetime.datetime]
        if isinstance(_as_of, Unset):
            as_of = UNSET
        else:
            as_of = isoparse(_as_of)

        def _parse_accounts(data: object) -> Union["BillingPriceListAccountsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                accounts_type_0 = BillingPriceListAccountsType0.from_dict(data)

                return accounts_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingPriceListAccountsType0", None, Unset], data)

        accounts = _parse_accounts(d.pop("accounts", UNSET))

        billing_price_list = cls(
            version=version,
            effective_from=effective_from,
            currency=currency,
            rule=rule,
            plans=plans,
            items=items,
            scope=scope,
            agreement=agreement,
            included=included,
            talk_to_sales_when=talk_to_sales_when,
            next_=next_,
            as_of=as_of,
            accounts=accounts,
        )

        billing_price_list.additional_properties = d
        return billing_price_list

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
