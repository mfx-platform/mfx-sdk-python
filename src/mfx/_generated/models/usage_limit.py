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

from ..models.usage_limit_source import UsageLimitSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageLimit")


@_attrs_define
class UsageLimit:
    """One limit: the figure in force, where it comes from, whether the platform applies it yet, and how much of it is in
    use where that is measured. Under `key` it is the figure for the calling key; under `tenant` the ceiling for all the
    tenant's keys together.

        Attributes:
            limit (int): Under `key`, for commands_per_s, commands_burst and ws_conns: the lower of the key's cap and the
                tenant's ceiling (a key with no cap may use the whole ceiling). A key whose commands_per_s cap applies and that
                has no commands_burst cap of its own bursts to twice that cap, never past the tenant's burst (source
                key_override, key_cap null). Otherwise the figure itself.
            source (UsageLimitSource): Where `limit` comes from. A tenant ceiling is the tenant's own figure, else the
                plan's. Under `key`, key_override when the key's own cap or figure is what applies.
            enforced (bool): False while the figure is published and not yet applied to this tenant: a request over it is
                not refused. True once it is: an execution command over its rate is 429 `rate_limited` with `Retry-After`, and
                the stream refuses, drops or closes as its limit says, naming the limit in `details.limit`.
            used (Union[None, int]): Current use where the platform measures it; null where it does not yet
            key_cap (Union[None, Unset, int]): Under `key`, for commands_per_s, commands_burst and ws_conns only: the key's
                own cap, null when the key has none (the default). Absent elsewhere.
    """

    limit: int
    source: UsageLimitSource
    enforced: bool
    used: Union[None, int]
    key_cap: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        source = self.source.value

        enforced = self.enforced

        used: Union[None, int]
        used = self.used

        key_cap: Union[None, Unset, int]
        if isinstance(self.key_cap, Unset):
            key_cap = UNSET
        else:
            key_cap = self.key_cap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "source": source,
                "enforced": enforced,
                "used": used,
            }
        )
        if key_cap is not UNSET:
            field_dict["key_cap"] = key_cap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit")

        source = UsageLimitSource(d.pop("source"))

        enforced = d.pop("enforced")

        def _parse_used(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        used = _parse_used(d.pop("used"))

        def _parse_key_cap(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        key_cap = _parse_key_cap(d.pop("key_cap", UNSET))

        usage_limit = cls(
            limit=limit,
            source=source,
            enforced=enforced,
            used=used,
            key_cap=key_cap,
        )

        usage_limit.additional_properties = d
        return usage_limit

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
