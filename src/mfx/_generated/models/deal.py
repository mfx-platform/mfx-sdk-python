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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.deal_close_reason_type_1 import DealCloseReasonType1
from ..models.deal_close_reason_type_2_type_1 import DealCloseReasonType2Type1
from ..models.deal_close_reason_type_3_type_1 import DealCloseReasonType3Type1
from ..models.deal_entry import DealEntry
from ..models.deal_side import DealSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="Deal")


@_attrs_define
class Deal:
    """
    Attributes:
        deal (int):
        order (Union[None, int]):
        position (Union[None, int]):
        symbol (str):
        side (DealSide):
        entry (DealEntry):
        volume (str):
        price (str):
        profit (str):
        commission (str):
        swap (str):
        time (datetime.datetime):
        magic (int):
        comment (str):
        close_reason (Union[DealCloseReasonType1, DealCloseReasonType2Type1, DealCloseReasonType3Type1, None]): MT5
            DEAL_REASON; null on an entry deal
        fee (Union[None, Unset, str]): The broker's fee on this deal (MT5 DEAL_FEE), in the account currency; null from
            a cell that does not send it
        balance (Union[None, Unset, str]): The account balance just after this deal, in the account currency: the
            balance when the history was read, less every deal after this one (profit, commission, swap and fee, balance
            deals included). Null when the cell could not read the later deals consistently
        sl (Union[None, Unset, str]): On a closing deal (`entry` out or inout), the stop loss the position had when it
            closed: the last one the platform recorded for it (position events and account snapshots). MT5 keeps no stop on
            a deal or on its closing order, so null on an entry deal, when the position had none, or when the platform never
            saw it open
        tp (Union[None, Unset, str]): As `sl`, for the take profit
    """

    deal: int
    order: Union[None, int]
    position: Union[None, int]
    symbol: str
    side: DealSide
    entry: DealEntry
    volume: str
    price: str
    profit: str
    commission: str
    swap: str
    time: datetime.datetime
    magic: int
    comment: str
    close_reason: Union[
        DealCloseReasonType1, DealCloseReasonType2Type1, DealCloseReasonType3Type1, None
    ]
    fee: Union[None, Unset, str] = UNSET
    balance: Union[None, Unset, str] = UNSET
    sl: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deal = self.deal

        order: Union[None, int]
        order = self.order

        position: Union[None, int]
        position = self.position

        symbol = self.symbol

        side = self.side.value

        entry = self.entry.value

        volume = self.volume

        price = self.price

        profit = self.profit

        commission = self.commission

        swap = self.swap

        time = self.time.isoformat()

        magic = self.magic

        comment = self.comment

        close_reason: Union[None, str]
        if isinstance(self.close_reason, DealCloseReasonType1):
            close_reason = self.close_reason.value
        elif isinstance(self.close_reason, DealCloseReasonType2Type1):
            close_reason = self.close_reason.value
        elif isinstance(self.close_reason, DealCloseReasonType3Type1):
            close_reason = self.close_reason.value
        else:
            close_reason = self.close_reason

        fee: Union[None, Unset, str]
        if isinstance(self.fee, Unset):
            fee = UNSET
        else:
            fee = self.fee

        balance: Union[None, Unset, str]
        if isinstance(self.balance, Unset):
            balance = UNSET
        else:
            balance = self.balance

        sl: Union[None, Unset, str]
        if isinstance(self.sl, Unset):
            sl = UNSET
        else:
            sl = self.sl

        tp: Union[None, Unset, str]
        if isinstance(self.tp, Unset):
            tp = UNSET
        else:
            tp = self.tp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deal": deal,
                "order": order,
                "position": position,
                "symbol": symbol,
                "side": side,
                "entry": entry,
                "volume": volume,
                "price": price,
                "profit": profit,
                "commission": commission,
                "swap": swap,
                "time": time,
                "magic": magic,
                "comment": comment,
                "close_reason": close_reason,
            }
        )
        if fee is not UNSET:
            field_dict["fee"] = fee
        if balance is not UNSET:
            field_dict["balance"] = balance
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deal = d.pop("deal")

        def _parse_order(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        order = _parse_order(d.pop("order"))

        def _parse_position(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        position = _parse_position(d.pop("position"))

        symbol = d.pop("symbol")

        side = DealSide(d.pop("side"))

        entry = DealEntry(d.pop("entry"))

        volume = d.pop("volume")

        price = d.pop("price")

        profit = d.pop("profit")

        commission = d.pop("commission")

        swap = d.pop("swap")

        time = isoparse(d.pop("time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        def _parse_close_reason(
            data: object,
        ) -> Union[
            DealCloseReasonType1, DealCloseReasonType2Type1, DealCloseReasonType3Type1, None
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                close_reason_type_1 = DealCloseReasonType1(data)

                return close_reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                close_reason_type_2_type_1 = DealCloseReasonType2Type1(data)

                return close_reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                close_reason_type_3_type_1 = DealCloseReasonType3Type1(data)

                return close_reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    DealCloseReasonType1, DealCloseReasonType2Type1, DealCloseReasonType3Type1, None
                ],
                data,
            )

        close_reason = _parse_close_reason(d.pop("close_reason"))

        def _parse_fee(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fee = _parse_fee(d.pop("fee", UNSET))

        def _parse_balance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        balance = _parse_balance(d.pop("balance", UNSET))

        def _parse_sl(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sl = _parse_sl(d.pop("sl", UNSET))

        def _parse_tp(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tp = _parse_tp(d.pop("tp", UNSET))

        deal = cls(
            deal=deal,
            order=order,
            position=position,
            symbol=symbol,
            side=side,
            entry=entry,
            volume=volume,
            price=price,
            profit=profit,
            commission=commission,
            swap=swap,
            time=time,
            magic=magic,
            comment=comment,
            close_reason=close_reason,
            fee=fee,
            balance=balance,
            sl=sl,
            tp=tp,
        )

        deal.additional_properties = d
        return deal

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
