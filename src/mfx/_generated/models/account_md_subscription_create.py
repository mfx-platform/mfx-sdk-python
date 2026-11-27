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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_md_subscription_create_timeframes_item import (
    AccountMdSubscriptionCreateTimeframesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountMdSubscriptionCreate")


@_attrs_define
class AccountMdSubscriptionCreate:
    """
    Attributes:
        symbol (str): As `GET /accounts/{id}/symbols` lists it
        timeframes (Union[Unset, list[AccountMdSubscriptionCreateTimeframesItem]]): Closed bars to stream on
            candles:{account_id}:{symbol}:{tf} and keep in the store; none means spots only. Asking again for the live
            subscription sets its timeframes to the ones asked, as POST /md/subscriptions does. Counted against the same
            series limit (409 bar_series_limit)
    """

    symbol: str
    timeframes: Union[Unset, list[AccountMdSubscriptionCreateTimeframesItem]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        timeframes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.timeframes, Unset):
            timeframes = []
            for timeframes_item_data in self.timeframes:
                timeframes_item = timeframes_item_data.value
                timeframes.append(timeframes_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "symbol": symbol,
            }
        )
        if timeframes is not UNSET:
            field_dict["timeframes"] = timeframes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        timeframes = []
        _timeframes = d.pop("timeframes", UNSET)
        for timeframes_item_data in _timeframes or []:
            timeframes_item = AccountMdSubscriptionCreateTimeframesItem._read(timeframes_item_data)

            timeframes.append(timeframes_item)

        account_md_subscription_create = cls(
            symbol=symbol,
            timeframes=timeframes,
        )

        return account_md_subscription_create
