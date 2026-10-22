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

from ..models.md_subscription_create_delivery import MdSubscriptionCreateDelivery
from ..models.md_subscription_create_timeframes_item import (
    MdSubscriptionCreateTimeframesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MdSubscriptionCreate")


@_attrs_define
class MdSubscriptionCreate:
    """
    Attributes:
        server_id (UUID): The broker is the server's own
        symbol (str): In the broker's own name, as the tenant's catalogue lists it
        timeframes (Union[Unset, list[MdSubscriptionCreateTimeframesItem]]): Candles to build; none means ticks only
        delivery (Union[Unset, MdSubscriptionCreateDelivery]):  Default: MdSubscriptionCreateDelivery.WS.
        connector_id (Union[None, UUID, Unset]): Required for redis_push, which is not yet available
    """

    server_id: UUID
    symbol: str
    timeframes: Union[Unset, list[MdSubscriptionCreateTimeframesItem]] = UNSET
    delivery: Union[Unset, MdSubscriptionCreateDelivery] = MdSubscriptionCreateDelivery.WS
    connector_id: Union[None, UUID, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        server_id = str(self.server_id)

        symbol = self.symbol

        timeframes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.timeframes, Unset):
            timeframes = []
            for timeframes_item_data in self.timeframes:
                timeframes_item = timeframes_item_data.value
                timeframes.append(timeframes_item)

        delivery: Union[Unset, str] = UNSET
        if not isinstance(self.delivery, Unset):
            delivery = self.delivery.value

        connector_id: Union[None, Unset, str]
        if isinstance(self.connector_id, Unset):
            connector_id = UNSET
        elif isinstance(self.connector_id, UUID):
            connector_id = str(self.connector_id)
        else:
            connector_id = self.connector_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "server_id": server_id,
                "symbol": symbol,
            }
        )
        if timeframes is not UNSET:
            field_dict["timeframes"] = timeframes
        if delivery is not UNSET:
            field_dict["delivery"] = delivery
        if connector_id is not UNSET:
            field_dict["connector_id"] = connector_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_id = UUID(d.pop("server_id"))

        symbol = d.pop("symbol")

        timeframes = []
        _timeframes = d.pop("timeframes", UNSET)
        for timeframes_item_data in _timeframes or []:
            timeframes_item = MdSubscriptionCreateTimeframesItem(timeframes_item_data)

            timeframes.append(timeframes_item)

        _delivery = d.pop("delivery", UNSET)
        delivery: Union[Unset, MdSubscriptionCreateDelivery]
        if isinstance(_delivery, Unset):
            delivery = UNSET
        else:
            delivery = MdSubscriptionCreateDelivery(_delivery)

        def _parse_connector_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                connector_id_type_0 = UUID(data)

                return connector_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        connector_id = _parse_connector_id(d.pop("connector_id", UNSET))

        md_subscription_create = cls(
            server_id=server_id,
            symbol=symbol,
            timeframes=timeframes,
            delivery=delivery,
            connector_id=connector_id,
        )

        return md_subscription_create
