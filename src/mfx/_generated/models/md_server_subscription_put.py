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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.md_server_subscription_put_interval_ms import (
    MdServerSubscriptionPutIntervalMs,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MdServerSubscriptionPut")


@_attrs_define
class MdServerSubscriptionPut:
    """
    Attributes:
        interval_ms (Union[Unset, MdServerSubscriptionPutIntervalMs]): How often the channel sends: each symbol's newest
            quote at most once per this many milliseconds Default: MdServerSubscriptionPutIntervalMs.VALUE_1000.
    """

    interval_ms: Union[Unset, MdServerSubscriptionPutIntervalMs] = (
        MdServerSubscriptionPutIntervalMs.VALUE_1000
    )

    def to_dict(self) -> dict[str, Any]:
        interval_ms: Union[Unset, int] = UNSET
        if not isinstance(self.interval_ms, Unset):
            interval_ms = self.interval_ms.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if interval_ms is not UNSET:
            field_dict["interval_ms"] = interval_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _interval_ms = d.pop("interval_ms", UNSET)
        interval_ms: Union[Unset, MdServerSubscriptionPutIntervalMs]
        if isinstance(_interval_ms, Unset):
            interval_ms = UNSET
        else:
            interval_ms = MdServerSubscriptionPutIntervalMs._read(_interval_ms)

        md_server_subscription_put = cls(
            interval_ms=interval_ms,
        )

        return md_server_subscription_put
