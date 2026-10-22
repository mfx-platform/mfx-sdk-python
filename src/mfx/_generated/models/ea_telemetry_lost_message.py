from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EaTelemetryLostMessage")


@_attrs_define
class EaTelemetryLostMessage:
    """`data` of an `expert_advisor.telemetry_lost` message on an `ea:` channel, in sequence where the records would have
    been: the EA wrote faster than its records could be delivered, the cell's allowance for the backlog was full, and
    the oldest waiting files were discarded. Trading is never held for telemetry.

        Attributes:
            schema_version (str): The payload's version; 1
            segment_from (int):
            segment_to (int):
            records (int): How many records the discarded files held
    """

    schema_version: str
    segment_from: int
    segment_to: int
    records: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        segment_from = self.segment_from

        segment_to = self.segment_to

        records = self.records

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "segment_from": segment_from,
                "segment_to": segment_to,
                "records": records,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        segment_from = d.pop("segment_from")

        segment_to = d.pop("segment_to")

        records = d.pop("records")

        ea_telemetry_lost_message = cls(
            schema_version=schema_version,
            segment_from=segment_from,
            segment_to=segment_to,
            records=records,
        )

        ea_telemetry_lost_message.additional_properties = d
        return ea_telemetry_lost_message

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
