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

if TYPE_CHECKING:
    from ..models.pending_order import PendingOrder
    from ..models.position import Position


T = TypeVar("T", bound="AccountSnapshotMessage")


@_attrs_define
class AccountSnapshotMessage:
    """`data` of an `account.snapshot` on `account:{terminal_id}`: the whole account. Replace your view with every
    snapshot, whatever its `seq`: the channel's `seq` starts again from 1 when the terminal has been quiet for 180 s.
    Sent on every `subscribe` and `resume` (the platform's current copy), when the position set changes (a ticket opens
    or closes, SL, TP or volume changes) and every 60 s while positions are open. Decimals are strings, as everywhere in
    this API.

        Attributes:
            terminal_id (UUID):
            schema_version (str): The payload's version; 1
            as_of (datetime.datetime): The cell's instant of the reading
            balance (str): Decimal as a string, in the account currency
            equity (str):
            margin (str):
            margin_free (str):
            margin_level (Union[None, str]): Null with no open positions
            open_positions_count (int):
            positions (list['Position']): Every open position, by ticket
            pending (list['PendingOrder']): Every pending order as of `pending_as_of`; empty when none was ever read
            pending_as_of (Union[None, datetime.datetime]): When the cell last read the pending orders (on a position
                change, or every 5 s); null when it never has
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
    positions: list["Position"]
    pending: list["PendingOrder"]
    pending_as_of: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pending_order import PendingOrder
        from ..models.position import Position

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

        positions = []
        for positions_item_data in self.positions:
            positions_item = positions_item_data.to_dict()
            positions.append(positions_item)

        pending = []
        for pending_item_data in self.pending:
            pending_item = pending_item_data.to_dict()
            pending.append(pending_item)

        pending_as_of: Union[None, str]
        if isinstance(self.pending_as_of, datetime.datetime):
            pending_as_of = self.pending_as_of.isoformat()
        else:
            pending_as_of = self.pending_as_of

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
                "positions": positions,
                "pending": pending,
                "pending_as_of": pending_as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pending_order import PendingOrder
        from ..models.position import Position

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

        positions = []
        _positions = d.pop("positions")
        for positions_item_data in _positions:
            positions_item = Position.from_dict(positions_item_data)

            positions.append(positions_item)

        pending = []
        _pending = d.pop("pending")
        for pending_item_data in _pending:
            pending_item = PendingOrder.from_dict(pending_item_data)

            pending.append(pending_item)

        def _parse_pending_as_of(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pending_as_of_type_0 = isoparse(data)

                return pending_as_of_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        pending_as_of = _parse_pending_as_of(d.pop("pending_as_of"))

        account_snapshot_message = cls(
            terminal_id=terminal_id,
            schema_version=schema_version,
            as_of=as_of,
            balance=balance,
            equity=equity,
            margin=margin,
            margin_free=margin_free,
            margin_level=margin_level,
            open_positions_count=open_positions_count,
            positions=positions,
            pending=pending,
            pending_as_of=pending_as_of,
        )

        account_snapshot_message.additional_properties = d
        return account_snapshot_message

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
