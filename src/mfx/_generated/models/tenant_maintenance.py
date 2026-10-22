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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_service import MaintenanceService
from ..models.tenant_maintenance_console import TenantMaintenanceConsole
from ..models.tenant_maintenance_state import TenantMaintenanceState
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantMaintenance")


@_attrs_define
class TenantMaintenance:
    """A maintenance window as a tenant of its scope sees it

    Attributes:
        id (UUID):
        label (str): MW-0031
        state (TenantMaintenanceState): in_progress covers running, paused and verifying; completed covers aborted
            (service restored)
        starts_at (datetime.datetime):
        ends_at (datetime.datetime): The current expected end: the ETA while in progress
        expected_minutes (int):
        started_at (Union[None, datetime.datetime]):
        ended_at (Union[None, datetime.datetime]):
        message (Union[None, str]): The tenant notification as scheduled, with this tenant's own counts; null when the
            notice is off
        suspended (list[MaintenanceService]): The services suspended for this tenant
        terminals (int): This tenant's terminals in scope: previewed before the start, resolved after
        console (TenantMaintenanceConsole): What the tenant console must do while it is in progress; normal otherwise
    """

    id: UUID
    label: str
    state: TenantMaintenanceState
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    expected_minutes: int
    started_at: Union[None, datetime.datetime]
    ended_at: Union[None, datetime.datetime]
    message: Union[None, str]
    suspended: list[MaintenanceService]
    terminals: int
    console: TenantMaintenanceConsole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        label = self.label

        state = self.state.value

        starts_at = self.starts_at.isoformat()

        ends_at = self.ends_at.isoformat()

        expected_minutes = self.expected_minutes

        started_at: Union[None, str]
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        ended_at: Union[None, str]
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        message: Union[None, str]
        message = self.message

        suspended = []
        for suspended_item_data in self.suspended:
            suspended_item = suspended_item_data.value
            suspended.append(suspended_item)

        terminals = self.terminals

        console = self.console.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "label": label,
                "state": state,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "expected_minutes": expected_minutes,
                "started_at": started_at,
                "ended_at": ended_at,
                "message": message,
                "suspended": suspended,
                "terminals": terminals,
                "console": console,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        label = d.pop("label")

        state = TenantMaintenanceState(d.pop("state"))

        starts_at = isoparse(d.pop("starts_at"))

        ends_at = isoparse(d.pop("ends_at"))

        expected_minutes = d.pop("expected_minutes")

        def _parse_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_ended_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = isoparse(data)

                return ended_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        def _parse_message(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        message = _parse_message(d.pop("message"))

        suspended = []
        _suspended = d.pop("suspended")
        for suspended_item_data in _suspended:
            suspended_item = MaintenanceService(suspended_item_data)

            suspended.append(suspended_item)

        terminals = d.pop("terminals")

        console = TenantMaintenanceConsole(d.pop("console"))

        tenant_maintenance = cls(
            id=id,
            label=label,
            state=state,
            starts_at=starts_at,
            ends_at=ends_at,
            expected_minutes=expected_minutes,
            started_at=started_at,
            ended_at=ended_at,
            message=message,
            suspended=suspended,
            terminals=terminals,
            console=console,
        )

        tenant_maintenance.additional_properties = d
        return tenant_maintenance

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
