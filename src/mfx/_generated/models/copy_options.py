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

from ..models.copy_options_when_risk_unchecked import CopyOptionsWhenRiskUnchecked
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyOptions")


@_attrs_define
class CopyOptions:
    """
    Attributes:
        reverse (Union[Unset, bool]): Copy the opposite side, with the stop loss and take profit swapped Default: False.
        copy_sl (Union[Unset, bool]):  Default: True.
        copy_tp (Union[Unset, bool]):  Default: True.
        copy_pending (Union[Unset, bool]): Place the leader's pending orders as pending orders. False copies one only
            when it fills, as a market entry. Needs a venue with pending orders Default: True.
        skip_pending (Union[Unset, bool]): Copy nothing that began as a pending order, even when it fills; logged
            skipped with skip_pending Default: False.
        close_only (Union[Unset, bool]): Copy closes only, so the follower winds down what it copied Default: False.
        delay_ms (Union[Unset, int]): Wait this long before sending each copy Default: 0.
        when_risk_unchecked (Union[Unset, CopyOptionsWhenRiskUnchecked]): When the follower account is protected by Risk
            Management (an active policy or a challenge in progress) and its copy host cannot yet check a copy against it:
            refuse refuses the copy with risk_rule (reason risk_inputs_stale); copy copies it unchecked. Once the host can
            check, every copy is checked whatever this says Default: CopyOptionsWhenRiskUnchecked.REFUSE.
    """

    reverse: Union[Unset, bool] = False
    copy_sl: Union[Unset, bool] = True
    copy_tp: Union[Unset, bool] = True
    copy_pending: Union[Unset, bool] = True
    skip_pending: Union[Unset, bool] = False
    close_only: Union[Unset, bool] = False
    delay_ms: Union[Unset, int] = 0
    when_risk_unchecked: Union[Unset, CopyOptionsWhenRiskUnchecked] = (
        CopyOptionsWhenRiskUnchecked.REFUSE
    )

    def to_dict(self) -> dict[str, Any]:
        reverse = self.reverse

        copy_sl = self.copy_sl

        copy_tp = self.copy_tp

        copy_pending = self.copy_pending

        skip_pending = self.skip_pending

        close_only = self.close_only

        delay_ms = self.delay_ms

        when_risk_unchecked: Union[Unset, str] = UNSET
        if not isinstance(self.when_risk_unchecked, Unset):
            when_risk_unchecked = self.when_risk_unchecked.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if reverse is not UNSET:
            field_dict["reverse"] = reverse
        if copy_sl is not UNSET:
            field_dict["copy_sl"] = copy_sl
        if copy_tp is not UNSET:
            field_dict["copy_tp"] = copy_tp
        if copy_pending is not UNSET:
            field_dict["copy_pending"] = copy_pending
        if skip_pending is not UNSET:
            field_dict["skip_pending"] = skip_pending
        if close_only is not UNSET:
            field_dict["close_only"] = close_only
        if delay_ms is not UNSET:
            field_dict["delay_ms"] = delay_ms
        if when_risk_unchecked is not UNSET:
            field_dict["when_risk_unchecked"] = when_risk_unchecked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reverse = d.pop("reverse", UNSET)

        copy_sl = d.pop("copy_sl", UNSET)

        copy_tp = d.pop("copy_tp", UNSET)

        copy_pending = d.pop("copy_pending", UNSET)

        skip_pending = d.pop("skip_pending", UNSET)

        close_only = d.pop("close_only", UNSET)

        delay_ms = d.pop("delay_ms", UNSET)

        _when_risk_unchecked = d.pop("when_risk_unchecked", UNSET)
        when_risk_unchecked: Union[Unset, CopyOptionsWhenRiskUnchecked]
        if isinstance(_when_risk_unchecked, Unset):
            when_risk_unchecked = UNSET
        else:
            when_risk_unchecked = CopyOptionsWhenRiskUnchecked._read(_when_risk_unchecked)

        copy_options = cls(
            reverse=reverse,
            copy_sl=copy_sl,
            copy_tp=copy_tp,
            copy_pending=copy_pending,
            skip_pending=skip_pending,
            close_only=close_only,
            delay_ms=delay_ms,
            when_risk_unchecked=when_risk_unchecked,
        )

        return copy_options
