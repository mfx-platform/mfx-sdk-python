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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyStages")


@_attrs_define
class CopyStages:
    """Milliseconds each stage took, each measured on its own machine. A stage that did not happen for this copy is absent.
    broker_ms is the venue's time and is not MFX Hub's.

        Attributes:
            detect_ms (Union[Unset, float]): Seeing the leader's deal
            sign_ms (Union[Unset, float]): Reporting and signing the signal
            deliver_ms (Union[Unset, float]): Delivering it to the follower's copy host
            expand_ms (Union[Unset, float]): Mapping, scaling and the risk check
            queue_ms (Union[Unset, float]): Waiting behind the follower account's own command
            hand_ms (Union[Unset, float]): Handing the order to the venue
            broker_ms (Union[Unset, float]): The venue's own time
    """

    detect_ms: Union[Unset, float] = UNSET
    sign_ms: Union[Unset, float] = UNSET
    deliver_ms: Union[Unset, float] = UNSET
    expand_ms: Union[Unset, float] = UNSET
    queue_ms: Union[Unset, float] = UNSET
    hand_ms: Union[Unset, float] = UNSET
    broker_ms: Union[Unset, float] = UNSET

    def to_dict(self) -> dict[str, Any]:
        detect_ms = self.detect_ms

        sign_ms = self.sign_ms

        deliver_ms = self.deliver_ms

        expand_ms = self.expand_ms

        queue_ms = self.queue_ms

        hand_ms = self.hand_ms

        broker_ms = self.broker_ms

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if detect_ms is not UNSET:
            field_dict["detect_ms"] = detect_ms
        if sign_ms is not UNSET:
            field_dict["sign_ms"] = sign_ms
        if deliver_ms is not UNSET:
            field_dict["deliver_ms"] = deliver_ms
        if expand_ms is not UNSET:
            field_dict["expand_ms"] = expand_ms
        if queue_ms is not UNSET:
            field_dict["queue_ms"] = queue_ms
        if hand_ms is not UNSET:
            field_dict["hand_ms"] = hand_ms
        if broker_ms is not UNSET:
            field_dict["broker_ms"] = broker_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detect_ms = d.pop("detect_ms", UNSET)

        sign_ms = d.pop("sign_ms", UNSET)

        deliver_ms = d.pop("deliver_ms", UNSET)

        expand_ms = d.pop("expand_ms", UNSET)

        queue_ms = d.pop("queue_ms", UNSET)

        hand_ms = d.pop("hand_ms", UNSET)

        broker_ms = d.pop("broker_ms", UNSET)

        copy_stages = cls(
            detect_ms=detect_ms,
            sign_ms=sign_ms,
            deliver_ms=deliver_ms,
            expand_ms=expand_ms,
            queue_ms=queue_ms,
            hand_ms=hand_ms,
            broker_ms=broker_ms,
        )

        return copy_stages
