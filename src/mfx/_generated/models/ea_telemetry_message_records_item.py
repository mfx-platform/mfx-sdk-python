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
    from ..models.ea_telemetry_message_records_item_record import (
        EaTelemetryMessageRecordsItemRecord,
    )


T = TypeVar("T", bound="EaTelemetryMessageRecordsItem")


@_attrs_define
class EaTelemetryMessageRecordsItem:
    """
    Attributes:
        segment (int): The number of the EA's telemetry file the record is from
        line (int): The record's line in that file
        record (EaTelemetryMessageRecordsItemRecord): The JSON object the EA wrote, as it wrote it. The platform does
            not read it for meaning, log it or store it
    """

    segment: int
    line: int
    record: "EaTelemetryMessageRecordsItemRecord"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_telemetry_message_records_item_record import (
            EaTelemetryMessageRecordsItemRecord,
        )

        segment = self.segment

        line = self.line

        record = self.record.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "segment": segment,
                "line": line,
                "record": record,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_telemetry_message_records_item_record import (
            EaTelemetryMessageRecordsItemRecord,
        )

        d = dict(src_dict)
        segment = d.pop("segment")

        line = d.pop("line")

        record = EaTelemetryMessageRecordsItemRecord.from_dict(d.pop("record"))

        ea_telemetry_message_records_item = cls(
            segment=segment,
            line=line,
            record=record,
        )

        ea_telemetry_message_records_item.additional_properties = d
        return ea_telemetry_message_records_item

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
