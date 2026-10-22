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

from ..models.symbol_spec_changed_change import SymbolSpecChangedChange
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.symbol_spec_changed_after_type_0 import SymbolSpecChangedAfterType0
    from ..models.symbol_spec_changed_before_type_0 import SymbolSpecChangedBeforeType0


T = TypeVar("T", bound="SymbolSpecChanged")


@_attrs_define
class SymbolSpecChanged:
    """`data` of a `symbol.spec_changed` message on the `events` channel: sent once for each change a tenant's terminal
    reported to a symbol on its own catalogue (one server and account type) - the specification a program sizes a trade
    by, what trading the broker allows, the trade sessions, or the symbol's removal. A pip value that moves with the
    exchange rate is not a change and sends nothing; read it on the catalogue. On the stream every value is text, and
    `before` and `after` are JSON objects as text.

        Attributes:
            schema_version (str):
            terminal_id (UUID): The join key: the terminal whose report showed the change. Every terminal of the tenant on
                that server and account type reads the same catalogue
            broker_id (UUID):
            server_id (UUID):
            account_type (str):
            symbol (str):
            change (SymbolSpecChangedChange):
            before (Union['SymbolSpecChangedBeforeType0', None]): The spec before (digits, contract_size, volume_min,
                volume_step, volume_max, trade_mode, margin_currency, pip_value_per_lot, trade_sessions, description), decimals
                as strings
            after (Union['SymbolSpecChangedAfterType0', None]): The spec after, same shape; null for a removal
            observed_at (datetime.datetime): When the terminal read its list
    """

    schema_version: str
    terminal_id: UUID
    broker_id: UUID
    server_id: UUID
    account_type: str
    symbol: str
    change: SymbolSpecChangedChange
    before: Union["SymbolSpecChangedBeforeType0", None]
    after: Union["SymbolSpecChangedAfterType0", None]
    observed_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.symbol_spec_changed_after_type_0 import (
            SymbolSpecChangedAfterType0,
        )
        from ..models.symbol_spec_changed_before_type_0 import (
            SymbolSpecChangedBeforeType0,
        )

        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        broker_id = str(self.broker_id)

        server_id = str(self.server_id)

        account_type = self.account_type

        symbol = self.symbol

        change = self.change.value

        before: Union[None, dict[str, Any]]
        if isinstance(self.before, SymbolSpecChangedBeforeType0):
            before = self.before.to_dict()
        else:
            before = self.before

        after: Union[None, dict[str, Any]]
        if isinstance(self.after, SymbolSpecChangedAfterType0):
            after = self.after.to_dict()
        else:
            after = self.after

        observed_at = self.observed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "broker_id": broker_id,
                "server_id": server_id,
                "account_type": account_type,
                "symbol": symbol,
                "change": change,
                "before": before,
                "after": after,
                "observed_at": observed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.symbol_spec_changed_after_type_0 import (
            SymbolSpecChangedAfterType0,
        )
        from ..models.symbol_spec_changed_before_type_0 import (
            SymbolSpecChangedBeforeType0,
        )

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        broker_id = UUID(d.pop("broker_id"))

        server_id = UUID(d.pop("server_id"))

        account_type = d.pop("account_type")

        symbol = d.pop("symbol")

        change = SymbolSpecChangedChange(d.pop("change"))

        def _parse_before(data: object) -> Union["SymbolSpecChangedBeforeType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                before_type_0 = SymbolSpecChangedBeforeType0.from_dict(data)

                return before_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SymbolSpecChangedBeforeType0", None], data)

        before = _parse_before(d.pop("before"))

        def _parse_after(data: object) -> Union["SymbolSpecChangedAfterType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                after_type_0 = SymbolSpecChangedAfterType0.from_dict(data)

                return after_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SymbolSpecChangedAfterType0", None], data)

        after = _parse_after(d.pop("after"))

        observed_at = isoparse(d.pop("observed_at"))

        symbol_spec_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            broker_id=broker_id,
            server_id=server_id,
            account_type=account_type,
            symbol=symbol,
            change=change,
            before=before,
            after=after,
            observed_at=observed_at,
        )

        symbol_spec_changed.additional_properties = d
        return symbol_spec_changed

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
