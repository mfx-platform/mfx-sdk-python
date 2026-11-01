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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_lifecycle_concurrency import UsageLifecycleConcurrency
    from ..models.usage_lifecycle_cooldown_s import UsageLifecycleCooldownS
    from ..models.usage_lifecycle_tenant_rate_per_hour import (
        UsageLifecycleTenantRatePerHour,
    )


T = TypeVar("T", bound="UsageLifecycle")


@_attrs_define
class UsageLifecycle:
    """The rules a terminal operation (restart, rebuild, move, retire, retry, attach, detach, drain) is refused by.

    Attributes:
        cooldown_s (UsageLifecycleCooldownS): Seconds a terminal rests after an operation of this kind; refused 429
            `cooldown`
        tenant_rate_per_hour (UsageLifecycleTenantRatePerHour): Operations of this kind and its kin per tenant per hour;
            refused 429 `tenant_rate`
        concurrency (UsageLifecycleConcurrency): Operations of this kind and its kin a tenant may have open at once;
            refused 429 `concurrency`
        farm_share (float): The share of a farm's terminals that may be in an operation at once (never fewer than one);
            refused 429 `farm_capacity`
        queue_max_wait_s (int): How long a refused operation may wait its turn
    """

    cooldown_s: "UsageLifecycleCooldownS"
    tenant_rate_per_hour: "UsageLifecycleTenantRatePerHour"
    concurrency: "UsageLifecycleConcurrency"
    farm_share: float
    queue_max_wait_s: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_lifecycle_concurrency import UsageLifecycleConcurrency
        from ..models.usage_lifecycle_cooldown_s import UsageLifecycleCooldownS
        from ..models.usage_lifecycle_tenant_rate_per_hour import (
            UsageLifecycleTenantRatePerHour,
        )

        cooldown_s = self.cooldown_s.to_dict()

        tenant_rate_per_hour = self.tenant_rate_per_hour.to_dict()

        concurrency = self.concurrency.to_dict()

        farm_share = self.farm_share

        queue_max_wait_s = self.queue_max_wait_s

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cooldown_s": cooldown_s,
                "tenant_rate_per_hour": tenant_rate_per_hour,
                "concurrency": concurrency,
                "farm_share": farm_share,
                "queue_max_wait_s": queue_max_wait_s,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_lifecycle_concurrency import UsageLifecycleConcurrency
        from ..models.usage_lifecycle_cooldown_s import UsageLifecycleCooldownS
        from ..models.usage_lifecycle_tenant_rate_per_hour import (
            UsageLifecycleTenantRatePerHour,
        )

        d = dict(src_dict)
        cooldown_s = UsageLifecycleCooldownS.from_dict(d.pop("cooldown_s"))

        tenant_rate_per_hour = UsageLifecycleTenantRatePerHour.from_dict(
            d.pop("tenant_rate_per_hour")
        )

        concurrency = UsageLifecycleConcurrency.from_dict(d.pop("concurrency"))

        farm_share = d.pop("farm_share")

        queue_max_wait_s = d.pop("queue_max_wait_s")

        usage_lifecycle = cls(
            cooldown_s=cooldown_s,
            tenant_rate_per_hour=tenant_rate_per_hour,
            concurrency=concurrency,
            farm_share=farm_share,
            queue_max_wait_s=queue_max_wait_s,
        )

        usage_lifecycle.additional_properties = d
        return usage_lifecycle

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
