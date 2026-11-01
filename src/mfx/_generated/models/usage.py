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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.usage_plan import UsagePlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_farms_item import UsageFarmsItem
    from ..models.usage_key import UsageKey
    from ..models.usage_lifecycle import UsageLifecycle
    from ..models.usage_per_login import UsagePerLogin
    from ..models.usage_tenant import UsageTenant
    from ..models.usage_webhooks import UsageWebhooks


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """The calling key's and its tenant's limits, each with where it comes from and how much of it is in use. Read it to
    pace an integration below the limits rather than finding them through 429s.

        Attributes:
            plan (UsagePlan): The tenant's plan, whose defaults apply where nothing is overridden
            key (UsageKey): The limits as they apply to the calling key. For commands_per_s, commands_burst and ws_conns
                that is the tenant's ceiling, lowered by the key's own cap where it has one.
            tenant (UsageTenant):
            farms (list['UsageFarmsItem']): The farms the tenant may place a terminal on, each with what one of its cells
                holds and how many terminals are on it now.
            per_login (UsagePerLogin): How many terminals may run on one broker login.
            lifecycle (UsageLifecycle): The rules a terminal operation (restart, rebuild, move, retire, retry, attach,
                detach, drain) is refused by.
            webhooks (UsageWebhooks):
            as_of (datetime.datetime):
    """

    plan: UsagePlan
    key: "UsageKey"
    tenant: "UsageTenant"
    farms: list["UsageFarmsItem"]
    per_login: "UsagePerLogin"
    lifecycle: "UsageLifecycle"
    webhooks: "UsageWebhooks"
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_farms_item import UsageFarmsItem
        from ..models.usage_key import UsageKey
        from ..models.usage_lifecycle import UsageLifecycle
        from ..models.usage_per_login import UsagePerLogin
        from ..models.usage_tenant import UsageTenant
        from ..models.usage_webhooks import UsageWebhooks

        plan = self.plan.value

        key = self.key.to_dict()

        tenant = self.tenant.to_dict()

        farms = []
        for farms_item_data in self.farms:
            farms_item = farms_item_data.to_dict()
            farms.append(farms_item)

        per_login = self.per_login.to_dict()

        lifecycle = self.lifecycle.to_dict()

        webhooks = self.webhooks.to_dict()

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
                "key": key,
                "tenant": tenant,
                "farms": farms,
                "per_login": per_login,
                "lifecycle": lifecycle,
                "webhooks": webhooks,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_farms_item import UsageFarmsItem
        from ..models.usage_key import UsageKey
        from ..models.usage_lifecycle import UsageLifecycle
        from ..models.usage_per_login import UsagePerLogin
        from ..models.usage_tenant import UsageTenant
        from ..models.usage_webhooks import UsageWebhooks

        d = dict(src_dict)
        plan = UsagePlan(d.pop("plan"))

        key = UsageKey.from_dict(d.pop("key"))

        tenant = UsageTenant.from_dict(d.pop("tenant"))

        farms = []
        _farms = d.pop("farms")
        for farms_item_data in _farms:
            farms_item = UsageFarmsItem.from_dict(farms_item_data)

            farms.append(farms_item)

        per_login = UsagePerLogin.from_dict(d.pop("per_login"))

        lifecycle = UsageLifecycle.from_dict(d.pop("lifecycle"))

        webhooks = UsageWebhooks.from_dict(d.pop("webhooks"))

        as_of = isoparse(d.pop("as_of"))

        usage = cls(
            plan=plan,
            key=key,
            tenant=tenant,
            farms=farms,
            per_login=per_login,
            lifecycle=lifecycle,
            webhooks=webhooks,
            as_of=as_of,
        )

        usage.additional_properties = d
        return usage

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
