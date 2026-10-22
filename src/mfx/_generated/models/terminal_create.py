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

from ..models.terminal_create_redundancy import TerminalCreateRedundancy
from ..models.terminal_create_refresh_ms import TerminalCreateRefreshMs
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.terminal_create_labels import TerminalCreateLabels


T = TypeVar("T", bound="TerminalCreate")


@_attrs_define
class TerminalCreate:
    """
    Attributes:
        broker_id (UUID):
        server_id (UUID): Must belong to broker_id; an unsupported server is 422
        farm_id (Union[Unset, UUID]): Optional. Omitted, the platform chooses: your own ACTIVE farms first, then shared
            ones (GET /farms lists both), offering the usages this terminal needs, in the server's region, with room; the
            oldest wins a tie. The choice is on the answer as `farm`. None fits is 409 no_farm
        streaming (Union[Unset, bool]): Publishes quotes (usage quote_streaming) Default: False.
        execution (Union[Unset, bool]): Accepts orders; needs a master credential Default: False.
        instruments (Union[Unset, list[str]]): Symbols to watch, in the broker's own names (e.g. EURUSD.sd). The farm's
            OS caps the count.
        labels (Union[Unset, TerminalCreateLabels]): Free-form, the tenant's own
        redundancy (Union[Unset, TerminalCreateRedundancy]):  Default: TerminalCreateRedundancy.NONE.
        refresh_ms (Union[Unset, TerminalCreateRefreshMs]): The terminal's refresh rate in milliseconds: how often it
            sweeps prices and, while positions are open, reads the account. Omitted, the farm's rate applies. Faster than
            the farm's rate is 422 with details.allowed. With no farm named, only farms that allow the rate are considered,
            and none with room is 409 no_farm (why no_room). A flat account is read every 60 s whatever this says
    """

    broker_id: UUID
    server_id: UUID
    farm_id: Union[Unset, UUID] = UNSET
    streaming: Union[Unset, bool] = False
    execution: Union[Unset, bool] = False
    instruments: Union[Unset, list[str]] = UNSET
    labels: Union[Unset, "TerminalCreateLabels"] = UNSET
    redundancy: Union[Unset, TerminalCreateRedundancy] = TerminalCreateRedundancy.NONE
    refresh_ms: Union[Unset, TerminalCreateRefreshMs] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.terminal_create_labels import TerminalCreateLabels

        broker_id = str(self.broker_id)

        server_id = str(self.server_id)

        farm_id: Union[Unset, str] = UNSET
        if not isinstance(self.farm_id, Unset):
            farm_id = str(self.farm_id)

        streaming = self.streaming

        execution = self.execution

        instruments: Union[Unset, list[str]] = UNSET
        if not isinstance(self.instruments, Unset):
            instruments = self.instruments

        labels: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        redundancy: Union[Unset, str] = UNSET
        if not isinstance(self.redundancy, Unset):
            redundancy = self.redundancy.value

        refresh_ms: Union[Unset, int] = UNSET
        if not isinstance(self.refresh_ms, Unset):
            refresh_ms = self.refresh_ms.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "broker_id": broker_id,
                "server_id": server_id,
            }
        )
        if farm_id is not UNSET:
            field_dict["farm_id"] = farm_id
        if streaming is not UNSET:
            field_dict["streaming"] = streaming
        if execution is not UNSET:
            field_dict["execution"] = execution
        if instruments is not UNSET:
            field_dict["instruments"] = instruments
        if labels is not UNSET:
            field_dict["labels"] = labels
        if redundancy is not UNSET:
            field_dict["redundancy"] = redundancy
        if refresh_ms is not UNSET:
            field_dict["refresh_ms"] = refresh_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.terminal_create_labels import TerminalCreateLabels

        d = dict(src_dict)
        broker_id = UUID(d.pop("broker_id"))

        server_id = UUID(d.pop("server_id"))

        _farm_id = d.pop("farm_id", UNSET)
        farm_id: Union[Unset, UUID]
        if isinstance(_farm_id, Unset):
            farm_id = UNSET
        else:
            farm_id = UUID(_farm_id)

        streaming = d.pop("streaming", UNSET)

        execution = d.pop("execution", UNSET)

        instruments = cast(list[str], d.pop("instruments", UNSET))

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, TerminalCreateLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = TerminalCreateLabels.from_dict(_labels)

        _redundancy = d.pop("redundancy", UNSET)
        redundancy: Union[Unset, TerminalCreateRedundancy]
        if isinstance(_redundancy, Unset):
            redundancy = UNSET
        else:
            redundancy = TerminalCreateRedundancy(_redundancy)

        _refresh_ms = d.pop("refresh_ms", UNSET)
        refresh_ms: Union[Unset, TerminalCreateRefreshMs]
        if isinstance(_refresh_ms, Unset):
            refresh_ms = UNSET
        else:
            refresh_ms = TerminalCreateRefreshMs(_refresh_ms)

        terminal_create = cls(
            broker_id=broker_id,
            server_id=server_id,
            farm_id=farm_id,
            streaming=streaming,
            execution=execution,
            instruments=instruments,
            labels=labels,
            redundancy=redundancy,
            refresh_ms=refresh_ms,
        )

        return terminal_create
