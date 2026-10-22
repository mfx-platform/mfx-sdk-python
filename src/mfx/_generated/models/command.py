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

from ..models.command_kind import CommandKind
from ..models.command_state import CommandState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_result import CommandResult


T = TypeVar("T", bound="Command")


@_attrs_define
class Command:
    """
    Attributes:
        command_id (UUID):
        terminal_id (UUID):
        kind (CommandKind):
        state (CommandState): Final states are SUCCEEDED, FAILED, EXPIRED and REJECTED. UNKNOWN is visible and NOT
            final: the order may have reached the broker and its outcome could not be read (a timeout after send, a lost
            connection). Reconciliation against the terminal's deal history resolves it to SUCCEEDED or FAILED on its own. A
            client must not re-send an order whose command is UNKNOWN, because that is how one fill becomes two. A
            NOT_EXECUTED answer from the terminal reads REJECTED with its reason. SUCCEEDED means the broker did what the
            command asked: for a market order, filled; for a pending order (limit, stop, stop_limit), accepted onto the
            broker's book with its ticket in `tickets.order` - not filled (OrderPlace).
        final (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        result (Union['CommandResult', None]): Null until the command has an outcome
        expires_at (Union[None, Unset, datetime.datetime]): After this the command is EXPIRED and never executes: a cell
            refuses an envelope past it, and a command still on the platform is swept EXPIRED. It is the command's deadline
            to reach the broker, not a pending order's own `expires_at`. Set from the moment the command is accepted, by
            kind: 10 s for every execution kind (order_place, order_cancel, order_modify, position_modify, position_close,
            position_close_partial, position_close_by, trailing_stop_set, trailing_stop_clear); an order_place may ask for 1
            s to 60 s instead with `expires_in_ms`
    """

    command_id: UUID
    terminal_id: UUID
    kind: CommandKind
    state: CommandState
    final: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    result: Union["CommandResult", None]
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.command_result import CommandResult

        command_id = str(self.command_id)

        terminal_id = str(self.terminal_id)

        kind = self.kind.value

        state = self.state.value

        final = self.final

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        result: Union[None, dict[str, Any]]
        if isinstance(self.result, CommandResult):
            result = self.result.to_dict()
        else:
            result = self.result

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command_id": command_id,
                "terminal_id": terminal_id,
                "kind": kind,
                "state": state,
                "final": final,
                "created_at": created_at,
                "updated_at": updated_at,
                "result": result,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.command_result import CommandResult

        d = dict(src_dict)
        command_id = UUID(d.pop("command_id"))

        terminal_id = UUID(d.pop("terminal_id"))

        kind = CommandKind(d.pop("kind"))

        state = CommandState(d.pop("state"))

        final = d.pop("final")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_result(data: object) -> Union["CommandResult", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = CommandResult.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CommandResult", None], data)

        result = _parse_result(d.pop("result"))

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        command = cls(
            command_id=command_id,
            terminal_id=terminal_id,
            kind=kind,
            state=state,
            final=final,
            created_at=created_at,
            updated_at=updated_at,
            result=result,
            expires_at=expires_at,
        )

        command.additional_properties = d
        return command

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
