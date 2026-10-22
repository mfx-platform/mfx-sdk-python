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

from ..models.command_state import CommandState
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandAccepted")


@_attrs_define
class CommandAccepted:
    """The answer to an accepted command: `{command_id, state, duplicate}`

    Attributes:
        command_id (UUID):
        state (CommandState): Final states are SUCCEEDED, FAILED, EXPIRED and REJECTED. UNKNOWN is visible and NOT
            final: the order may have reached the broker and its outcome could not be read (a timeout after send, a lost
            connection). Reconciliation against the terminal's deal history resolves it to SUCCEEDED or FAILED on its own. A
            client must not re-send an order whose command is UNKNOWN, because that is how one fill becomes two. A
            NOT_EXECUTED answer from the terminal reads REJECTED with its reason. SUCCEEDED means the broker did what the
            command asked: for a market order, filled; for a pending order (limit, stop, stop_limit), accepted onto the
            broker's book with its ticket in `tickets.order` - not filled (OrderPlace).
        duplicate (bool): True when this Idempotency-Key was seen before; the original command is returned, never re-
            executed
        expires_at (Union[Unset, datetime.datetime]): After this the command is EXPIRED and never executes: a cell
            refuses an envelope past it, and a command still on the platform is swept EXPIRED. It is the command's deadline
            to reach the broker, not a pending order's own `expires_at`. Set from the moment the command is accepted, by
            kind: 10 s for every execution kind (order_place, order_cancel, order_modify, position_modify, position_close,
            position_close_partial, position_close_by, trailing_stop_set, trailing_stop_clear); an order_place may ask for 1
            s to 60 s instead with `expires_in_ms`
    """

    command_id: UUID
    state: CommandState
    duplicate: bool
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command_id = str(self.command_id)

        state = self.state.value

        duplicate = self.duplicate

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command_id": command_id,
                "state": state,
                "duplicate": duplicate,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        command_id = UUID(d.pop("command_id"))

        state = CommandState(d.pop("state"))

        duplicate = d.pop("duplicate")

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        command_accepted = cls(
            command_id=command_id,
            state=state,
            duplicate=duplicate,
            expires_at=expires_at,
        )

        command_accepted.additional_properties = d
        return command_accepted

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
