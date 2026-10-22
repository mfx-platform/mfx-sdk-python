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

from ..models.tenant_maintenance_terminal_state import TenantMaintenanceTerminalState
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantMaintenanceTerminal")


@_attrs_define
class TenantMaintenanceTerminal:
    """
    Attributes:
        terminal_id (UUID):
        state (TenantMaintenanceTerminalState): waiting for its batch; migrating (moving to a new machine, or
            restarting); back; attention (did not come back, an operator is on it)
        since (Union[None, datetime.datetime]):
        eta_at (Union[None, datetime.datetime]): When this terminal is expected back: its batch's expected end while
            migrating, its batch's expected start plus a batch while waiting
    """

    terminal_id: UUID
    state: TenantMaintenanceTerminalState
    since: Union[None, datetime.datetime]
    eta_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_id = str(self.terminal_id)

        state = self.state.value

        since: Union[None, str]
        if isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        eta_at: Union[None, str]
        if isinstance(self.eta_at, datetime.datetime):
            eta_at = self.eta_at.isoformat()
        else:
            eta_at = self.eta_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "state": state,
                "since": since,
                "eta_at": eta_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        state = TenantMaintenanceTerminalState(d.pop("state"))

        def _parse_since(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        since = _parse_since(d.pop("since"))

        def _parse_eta_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                eta_at_type_0 = isoparse(data)

                return eta_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        eta_at = _parse_eta_at(d.pop("eta_at"))

        tenant_maintenance_terminal = cls(
            terminal_id=terminal_id,
            state=state,
            since=since,
            eta_at=eta_at,
        )

        tenant_maintenance_terminal.additional_properties = d
        return tenant_maintenance_terminal

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
