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
    from ..models.ea_telemetry_message_records_item import EaTelemetryMessageRecordsItem


T = TypeVar("T", bound="EaTelemetryMessage")


@_attrs_define
class EaTelemetryMessage:
    """`data` of an `expert_advisor.telemetry` message on an `ea:` channel: a batch of records the tenant's EA wrote, in
    the order written. Delivery is at least once: after the cell restarts a file is sent again from its start, and
    `segment` with `line` is what a client drops a repeat on. `skipped` and `dropped` are counts since the message
    before, so nothing is left out in silence.

        Attributes:
            schema_version (str): The payload's version; 1
            records (list['EaTelemetryMessageRecordsItem']):
            skipped (int): Lines the cell could not read: too long, too deep or not JSON
            dropped (int): Records the platform left out: over the largest record, deeper than eight levels, or over the
                terminal's pace for the minute
    """

    schema_version: str
    records: list["EaTelemetryMessageRecordsItem"]
    skipped: int
    dropped: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_telemetry_message_records_item import (
            EaTelemetryMessageRecordsItem,
        )

        schema_version = self.schema_version

        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()
            records.append(records_item)

        skipped = self.skipped

        dropped = self.dropped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "records": records,
                "skipped": skipped,
                "dropped": dropped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_telemetry_message_records_item import (
            EaTelemetryMessageRecordsItem,
        )

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = EaTelemetryMessageRecordsItem.from_dict(records_item_data)

            records.append(records_item)

        skipped = d.pop("skipped")

        dropped = d.pop("dropped")

        ea_telemetry_message = cls(
            schema_version=schema_version,
            records=records,
            skipped=skipped,
            dropped=dropped,
        )

        ea_telemetry_message.additional_properties = d
        return ea_telemetry_message

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
