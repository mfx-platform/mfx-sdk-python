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

from ..models.md_server_subscription_interval_ms import MdServerSubscriptionIntervalMs
from ..models.md_server_subscription_state import MdServerSubscriptionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref import Ref


T = TypeVar("T", bound="MdServerSubscription")


@_attrs_define
class MdServerSubscription:
    """The tenant's subscription to a whole server's quotes, one per server. It covers every symbol the tenant's terminals
    on that server read, now and later, and names none; it adds no symbol to any terminal. Its channel is
    `md:{server_id}`. A stopped subscription is gone: `GET` answers 404 and a later `PUT` makes a new one.

        Attributes:
            id (UUID):
            broker (Ref): A resolved foreign key — enough to render and link, never a second fetch.
            server (Ref): A resolved foreign key — enough to render and link, never a second fetch.
            interval_ms (MdServerSubscriptionIntervalMs):
            state (MdServerSubscriptionState): `pending` until the platform has written the first quote for its channel,
                then `streaming`
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            symbols (Union[None, Unset, int]): How many symbols the platform holds a quote for on this server now; null when
                it cannot tell
            first_quote_at (Union[None, Unset, datetime.datetime]):
    """

    id: UUID
    broker: "Ref"
    server: "Ref"
    interval_ms: MdServerSubscriptionIntervalMs
    state: MdServerSubscriptionState
    created_at: datetime.datetime
    updated_at: datetime.datetime
    symbols: Union[None, Unset, int] = UNSET
    first_quote_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref

        id = str(self.id)

        broker = self.broker.to_dict()

        server = self.server.to_dict()

        interval_ms = self.interval_ms.value

        state = self.state.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        symbols: Union[None, Unset, int]
        if isinstance(self.symbols, Unset):
            symbols = UNSET
        else:
            symbols = self.symbols

        first_quote_at: Union[None, Unset, str]
        if isinstance(self.first_quote_at, Unset):
            first_quote_at = UNSET
        elif isinstance(self.first_quote_at, datetime.datetime):
            first_quote_at = self.first_quote_at.isoformat()
        else:
            first_quote_at = self.first_quote_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "broker": broker,
                "server": server,
                "interval_ms": interval_ms,
                "state": state,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if symbols is not UNSET:
            field_dict["symbols"] = symbols
        if first_quote_at is not UNSET:
            field_dict["first_quote_at"] = first_quote_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        broker = Ref.from_dict(d.pop("broker"))

        server = Ref.from_dict(d.pop("server"))

        interval_ms = MdServerSubscriptionIntervalMs._read(d.pop("interval_ms"))

        state = MdServerSubscriptionState._read(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_symbols(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        symbols = _parse_symbols(d.pop("symbols", UNSET))

        def _parse_first_quote_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_quote_at_type_0 = isoparse(data)

                return first_quote_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        first_quote_at = _parse_first_quote_at(d.pop("first_quote_at", UNSET))

        md_server_subscription = cls(
            id=id,
            broker=broker,
            server=server,
            interval_ms=interval_ms,
            state=state,
            created_at=created_at,
            updated_at=updated_at,
            symbols=symbols,
            first_quote_at=first_quote_at,
        )

        md_server_subscription.additional_properties = d
        return md_server_subscription

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
