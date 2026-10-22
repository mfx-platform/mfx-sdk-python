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

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountMarksMessage")


@_attrs_define
class AccountMarksMessage:
    """`data` of an `account.marks` on `account:{terminal_id}`: between snapshots, at the terminal's refresh rate while
    positions are open and only when something moved, the figures and one mark per position whose values changed since
    the last message. Every 5 s with nothing moved, a keep-alive: the figures and an empty `marks`. Apply it only to the
    snapshot its `base` names (`StreamServerMessage.base`): set each ticket's `price_current`, `profit` and `swap`, and
    the figures. A ticket you do not hold means your view is behind: ignore the message and resume, or wait for the next
    snapshot.

        Attributes:
            terminal_id (UUID):
            schema_version (str): The payload's version; 1
            as_of (datetime.datetime):
            balance (str):
            equity (str):
            margin (str):
            margin_free (str):
            margin_level (Union[None, str]):
            open_positions_count (int): The snapshot's: a change in the position set is sent as a snapshot, never as marks
            marks (list[list[Union[int, str]]]): One `[ticket, price_current, profit, swap]` per moved position; empty on a
                keep-alive
    """

    terminal_id: UUID
    schema_version: str
    as_of: datetime.datetime
    balance: str
    equity: str
    margin: str
    margin_free: str
    margin_level: Union[None, str]
    open_positions_count: int
    marks: list[list[Union[int, str]]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_id = str(self.terminal_id)

        schema_version = self.schema_version

        as_of = self.as_of.isoformat()

        balance = self.balance

        equity = self.equity

        margin = self.margin

        margin_free = self.margin_free

        margin_level: Union[None, str]
        margin_level = self.margin_level

        open_positions_count = self.open_positions_count

        marks = []
        for marks_item_data in self.marks:
            marks_item = []
            for marks_item_item_data in marks_item_data:
                marks_item_item: Union[int, str]
                marks_item_item = marks_item_item_data
                marks_item.append(marks_item_item)

            marks.append(marks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "schema_version": schema_version,
                "as_of": as_of,
                "balance": balance,
                "equity": equity,
                "margin": margin,
                "margin_free": margin_free,
                "margin_level": margin_level,
                "open_positions_count": open_positions_count,
                "marks": marks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        schema_version = d.pop("schema_version")

        as_of = isoparse(d.pop("as_of"))

        balance = d.pop("balance")

        equity = d.pop("equity")

        margin = d.pop("margin")

        margin_free = d.pop("margin_free")

        def _parse_margin_level(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        margin_level = _parse_margin_level(d.pop("margin_level"))

        open_positions_count = d.pop("open_positions_count")

        marks = []
        _marks = d.pop("marks")
        for marks_item_data in _marks:
            marks_item = []
            _marks_item = marks_item_data
            for marks_item_item_data in _marks_item:

                def _parse_marks_item_item(data: object) -> Union[int, str]:
                    return cast(Union[int, str], data)

                marks_item_item = _parse_marks_item_item(marks_item_item_data)

                marks_item.append(marks_item_item)

            marks.append(marks_item)

        account_marks_message = cls(
            terminal_id=terminal_id,
            schema_version=schema_version,
            as_of=as_of,
            balance=balance,
            equity=equity,
            margin=margin,
            margin_free=margin_free,
            margin_level=margin_level,
            open_positions_count=open_positions_count,
            marks=marks,
        )

        account_marks_message.additional_properties = d
        return account_marks_message

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
