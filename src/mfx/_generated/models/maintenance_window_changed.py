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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_window_changed_change import MaintenanceWindowChangedChange
from ..models.maintenance_window_changed_state import MaintenanceWindowChangedState
from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceWindowChanged")


@_attrs_define
class MaintenanceWindowChanged:
    """`data` of a `maintenance.window_changed` message on the `events` channel, and the same event to webhooks: sent when
    a window is announced to you, starts, its expected end or its message changes, ends or is cancelled. The fields are
    those of `TenantMaintenance`, as the window stands after the change; `GET /maintenance` answers the same. On the
    stream every value is text, as on every event.

        Example:
            {'schema_version': '1', 'window_id': '5b1d7e0a-2c44-4f0e-9a51-7d3b8c6e1f20', 'label': 'MW-0031', 'state':
                'in_progress', 'starts_at': '2026-11-05T10:00:00Z', 'ends_at': '2026-11-05T12:00:00Z', 'message': 'Planned
                maintenance on 3 of your terminals until about 12:00 UTC', 'terminals': '3', 'change': 'eta_moved'}

        Attributes:
            schema_version (str): The payload's version; 1
            window_id (UUID):
            label (str): MW-0031
            state (MaintenanceWindowChangedState):
            starts_at (datetime.datetime):
            ends_at (datetime.datetime): The current expected end: the ETA while in progress
            message (str): The notice as sent to you, with your own counts; empty when the notice is off
            terminals (str): How many of your terminals are in the window; GET /maintenance/{id}/terminals lists them, each
                with its own expected time
            change (MaintenanceWindowChangedChange): What moved this time
    """

    schema_version: str
    window_id: UUID
    label: str
    state: MaintenanceWindowChangedState
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    message: str
    terminals: str
    change: MaintenanceWindowChangedChange
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        window_id = str(self.window_id)

        label = self.label

        state = self.state.value

        starts_at = self.starts_at.isoformat()

        ends_at = self.ends_at.isoformat()

        message = self.message

        terminals = self.terminals

        change = self.change.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "window_id": window_id,
                "label": label,
                "state": state,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "message": message,
                "terminals": terminals,
                "change": change,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        window_id = UUID(d.pop("window_id"))

        label = d.pop("label")

        state = MaintenanceWindowChangedState(d.pop("state"))

        starts_at = isoparse(d.pop("starts_at"))

        ends_at = isoparse(d.pop("ends_at"))

        message = d.pop("message")

        terminals = d.pop("terminals")

        change = MaintenanceWindowChangedChange(d.pop("change"))

        maintenance_window_changed = cls(
            schema_version=schema_version,
            window_id=window_id,
            label=label,
            state=state,
            starts_at=starts_at,
            ends_at=ends_at,
            message=message,
            terminals=terminals,
            change=change,
        )

        maintenance_window_changed.additional_properties = d
        return maintenance_window_changed

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
