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

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkTerminalAsk")


@_attrs_define
class BulkTerminalAsk:
    """Which of your terminals a bulk restart or retire takes, and why. At least one of the filters; given together they
    narrow each other

        Attributes:
            reason (str): Why; written to the audit log and to each item
            farm_id (Union[None, UUID, Unset]): Every terminal of yours on this farm
            broker_id (Union[None, UUID, Unset]): Every terminal of yours on this broker
            terminal_ids (Union[None, Unset, list[UUID]]): These terminals
            confirm_open_positions (Union[Unset, bool]): Rule 3, as on TerminalRestart, for every terminal taken: without it
                a terminal with open positions is refused (`refused[].code = positions_open`) and the rest are taken Default:
                False.
    """

    reason: str
    farm_id: Union[None, UUID, Unset] = UNSET
    broker_id: Union[None, UUID, Unset] = UNSET
    terminal_ids: Union[None, Unset, list[UUID]] = UNSET
    confirm_open_positions: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        farm_id: Union[None, Unset, str]
        if isinstance(self.farm_id, Unset):
            farm_id = UNSET
        elif isinstance(self.farm_id, UUID):
            farm_id = str(self.farm_id)
        else:
            farm_id = self.farm_id

        broker_id: Union[None, Unset, str]
        if isinstance(self.broker_id, Unset):
            broker_id = UNSET
        elif isinstance(self.broker_id, UUID):
            broker_id = str(self.broker_id)
        else:
            broker_id = self.broker_id

        terminal_ids: Union[None, Unset, list[str]]
        if isinstance(self.terminal_ids, Unset):
            terminal_ids = UNSET
        elif isinstance(self.terminal_ids, list):
            terminal_ids = []
            for terminal_ids_type_0_item_data in self.terminal_ids:
                terminal_ids_type_0_item = str(terminal_ids_type_0_item_data)
                terminal_ids.append(terminal_ids_type_0_item)

        else:
            terminal_ids = self.terminal_ids

        confirm_open_positions = self.confirm_open_positions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "reason": reason,
            }
        )
        if farm_id is not UNSET:
            field_dict["farm_id"] = farm_id
        if broker_id is not UNSET:
            field_dict["broker_id"] = broker_id
        if terminal_ids is not UNSET:
            field_dict["terminal_ids"] = terminal_ids
        if confirm_open_positions is not UNSET:
            field_dict["confirm_open_positions"] = confirm_open_positions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        def _parse_farm_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                farm_id_type_0 = UUID(data)

                return farm_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        farm_id = _parse_farm_id(d.pop("farm_id", UNSET))

        def _parse_broker_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                broker_id_type_0 = UUID(data)

                return broker_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        broker_id = _parse_broker_id(d.pop("broker_id", UNSET))

        def _parse_terminal_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                terminal_ids_type_0 = []
                _terminal_ids_type_0 = data
                for terminal_ids_type_0_item_data in _terminal_ids_type_0:
                    terminal_ids_type_0_item = UUID(terminal_ids_type_0_item_data)

                    terminal_ids_type_0.append(terminal_ids_type_0_item)

                return terminal_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        terminal_ids = _parse_terminal_ids(d.pop("terminal_ids", UNSET))

        confirm_open_positions = d.pop("confirm_open_positions", UNSET)

        bulk_terminal_ask = cls(
            reason=reason,
            farm_id=farm_id,
            broker_id=broker_id,
            terminal_ids=terminal_ids,
            confirm_open_positions=confirm_open_positions,
        )

        return bulk_terminal_ask
