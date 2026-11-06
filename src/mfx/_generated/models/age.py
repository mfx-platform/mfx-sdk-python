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

from ..types import UNSET, Unset

T = TypeVar("T", bound="Age")


@_attrs_define
class Age:
    """An observation with its age. `seconds` is null when the observation is missing — which reads as UNKNOWN, never as
    zero and never as fresh (L14, L36, L43, guardrail 15).

        Attributes:
            at (Union[None, datetime.datetime]):
            seconds (Union[None, int]):
            stale (Union[Unset, bool]): The observation is older than its metric's freshness bound, so it is unknown. For a
                cell's heartbeat the bound is the heartbeat's red line (`vitals.heartbeat_age_s.red`): the list, the Overview
                and the tile turn at the moment the SLA says down.
    """

    at: Union[None, datetime.datetime]
    seconds: Union[None, int]
    stale: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at: Union[None, str]
        if isinstance(self.at, datetime.datetime):
            at = self.at.isoformat()
        else:
            at = self.at

        seconds: Union[None, int]
        seconds = self.seconds

        stale = self.stale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "seconds": seconds,
            }
        )
        if stale is not UNSET:
            field_dict["stale"] = stale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_type_0 = isoparse(data)

                return at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        at = _parse_at(d.pop("at"))

        def _parse_seconds(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        seconds = _parse_seconds(d.pop("seconds"))

        stale = d.pop("stale", UNSET)

        age = cls(
            at=at,
            seconds=seconds,
            stale=stale,
        )

        age.additional_properties = d
        return age

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
