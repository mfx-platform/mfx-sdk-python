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

from ..models.symbol_filling_modes_type_0_item import SymbolFillingModesType0Item
from ..models.symbol_swap_type_type_1 import SymbolSwapTypeType1
from ..models.symbol_swap_type_type_2_type_1 import SymbolSwapTypeType2Type1
from ..models.symbol_swap_type_type_3_type_1 import SymbolSwapTypeType3Type1
from ..models.symbol_trade_mode import SymbolTradeMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.symbol_status import SymbolStatus
    from ..models.trade_session import TradeSession


T = TypeVar("T", bound="Symbol")


@_attrs_define
class Symbol:
    """
    Attributes:
        symbol (str):
        description (str):
        server_id (UUID):
        account_type (str):
        digits (int):
        contract_size (str): decimal as a string
        volume_min (str):
        volume_max (str):
        volume_step (str):
        trade_mode (SymbolTradeMode):
        margin_currency (str):
        pip_value_per_lot (Union[None, str]): from the terminal, never derived. A quote figure, not part of the
            specification: it moves with the exchange rate, is kept within the platform's tolerance of the terminal's own
            value for a watched symbol, and neither moves spec_hash nor raises symbol.spec_changed
        spec_hash (str): changes drive symbol.spec_changed. Taken over digits, contract_size, volume_min, volume_max,
            volume_step, trade_mode, margin_currency, profit_currency, point, tick_size, stops_level, freeze_level,
            swap_long, swap_short, swap_type, margin_initial, margin_maintenance and filling_modes; not over the quote
            figures pip_value_per_lot, tick_value and margin_per_lot
        trade_sessions (Union[None, list['TradeSession']]): null when the terminal could not report sessions;
            closed_session is then never derived
        refreshed_at (datetime.datetime):
        status (SymbolStatus):
        profit_currency (Union[None, Unset, str]): The currency the profit is computed in (SYMBOL_CURRENCY_PROFIT).
        point (Union[None, Unset, str]): One point, the smallest price step the symbol is quoted in (SYMBOL_POINT):
            0.00001 on a five-digit FX pair.
        tick_size (Union[None, Unset, str]): The smallest price change a price may make (SYMBOL_TRADE_TICK_SIZE); a
            price off it is put on it by the snap rule.
        tick_value (Union[None, Unset, str]): What one tick is worth on one lot, in the account currency
            (SYMBOL_TRADE_TICK_VALUE). A quote figure like pip_value_per_lot: it moves with the exchange rate where the
            profit currency is not the account's, and it is not in spec_hash.
        stops_level (Union[None, Unset, int]): How close to the current price, in points, a stop loss, a take profit or
            a pending price may be set (SYMBOL_TRADE_STOPS_LEVEL); 0 means the broker sets no minimum.
        freeze_level (Union[None, Unset, int]): How close to the current price, in points, a pending order or a
            position's stops can no longer be changed (SYMBOL_TRADE_FREEZE_LEVEL); 0 means none.
        swap_long (Union[None, Unset, str]): The swap a buy position pays or earns a night, in the unit swap_type names
            (SYMBOL_SWAP_LONG).
        swap_short (Union[None, Unset, str]): As swap_long, for a sell position (SYMBOL_SWAP_SHORT)
        swap_type (Union[None, SymbolSwapTypeType1, SymbolSwapTypeType2Type1, SymbolSwapTypeType3Type1, Unset]): The
            unit of swap_long and swap_short (MT5 SYMBOL_SWAP_MODE 0-8, lower-cased).
        margin_initial (Union[None, Unset, str]): The broker's initial margin setting for one lot
            (SYMBOL_MARGIN_INITIAL), in the unit the symbol's margin calculation mode uses; 0 when the broker leaves it to
            the calculation mode. To pre-check margin read margin_per_lot.
        margin_maintenance (Union[None, Unset, str]): As margin_initial, the maintenance margin
            (SYMBOL_MARGIN_MAINTENANCE)
        margin_per_lot (Union[None, Unset, str]): The margin one lot bought at the current ask holds, in the account
            currency, as the terminal computes it (order_calc_margin) with this account's leverage. A quote figure like
            pip_value_per_lot: it moves with price and is not in spec_hash.
        filling_modes (Union[None, Unset, list[SymbolFillingModesType0Item]]): The fill policies the broker allows
            besides return (SYMBOL_FILLING_MODE flags: fill or kill, immediate or cancel, book or cancel).
    """

    symbol: str
    description: str
    server_id: UUID
    account_type: str
    digits: int
    contract_size: str
    volume_min: str
    volume_max: str
    volume_step: str
    trade_mode: SymbolTradeMode
    margin_currency: str
    pip_value_per_lot: Union[None, str]
    spec_hash: str
    trade_sessions: Union[None, list["TradeSession"]]
    refreshed_at: datetime.datetime
    status: "SymbolStatus"
    profit_currency: Union[None, Unset, str] = UNSET
    point: Union[None, Unset, str] = UNSET
    tick_size: Union[None, Unset, str] = UNSET
    tick_value: Union[None, Unset, str] = UNSET
    stops_level: Union[None, Unset, int] = UNSET
    freeze_level: Union[None, Unset, int] = UNSET
    swap_long: Union[None, Unset, str] = UNSET
    swap_short: Union[None, Unset, str] = UNSET
    swap_type: Union[
        None, SymbolSwapTypeType1, SymbolSwapTypeType2Type1, SymbolSwapTypeType3Type1, Unset
    ] = UNSET
    margin_initial: Union[None, Unset, str] = UNSET
    margin_maintenance: Union[None, Unset, str] = UNSET
    margin_per_lot: Union[None, Unset, str] = UNSET
    filling_modes: Union[None, Unset, list[SymbolFillingModesType0Item]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.symbol_status import SymbolStatus
        from ..models.trade_session import TradeSession

        symbol = self.symbol

        description = self.description

        server_id = str(self.server_id)

        account_type = self.account_type

        digits = self.digits

        contract_size = self.contract_size

        volume_min = self.volume_min

        volume_max = self.volume_max

        volume_step = self.volume_step

        trade_mode = self.trade_mode.value

        margin_currency = self.margin_currency

        pip_value_per_lot: Union[None, str]
        pip_value_per_lot = self.pip_value_per_lot

        spec_hash = self.spec_hash

        trade_sessions: Union[None, list[dict[str, Any]]]
        if isinstance(self.trade_sessions, list):
            trade_sessions = []
            for trade_sessions_type_0_item_data in self.trade_sessions:
                trade_sessions_type_0_item = trade_sessions_type_0_item_data.to_dict()
                trade_sessions.append(trade_sessions_type_0_item)

        else:
            trade_sessions = self.trade_sessions

        refreshed_at = self.refreshed_at.isoformat()

        status = self.status.to_dict()

        profit_currency: Union[None, Unset, str]
        if isinstance(self.profit_currency, Unset):
            profit_currency = UNSET
        else:
            profit_currency = self.profit_currency

        point: Union[None, Unset, str]
        if isinstance(self.point, Unset):
            point = UNSET
        else:
            point = self.point

        tick_size: Union[None, Unset, str]
        if isinstance(self.tick_size, Unset):
            tick_size = UNSET
        else:
            tick_size = self.tick_size

        tick_value: Union[None, Unset, str]
        if isinstance(self.tick_value, Unset):
            tick_value = UNSET
        else:
            tick_value = self.tick_value

        stops_level: Union[None, Unset, int]
        if isinstance(self.stops_level, Unset):
            stops_level = UNSET
        else:
            stops_level = self.stops_level

        freeze_level: Union[None, Unset, int]
        if isinstance(self.freeze_level, Unset):
            freeze_level = UNSET
        else:
            freeze_level = self.freeze_level

        swap_long: Union[None, Unset, str]
        if isinstance(self.swap_long, Unset):
            swap_long = UNSET
        else:
            swap_long = self.swap_long

        swap_short: Union[None, Unset, str]
        if isinstance(self.swap_short, Unset):
            swap_short = UNSET
        else:
            swap_short = self.swap_short

        swap_type: Union[None, Unset, str]
        if isinstance(self.swap_type, Unset):
            swap_type = UNSET
        elif isinstance(self.swap_type, SymbolSwapTypeType1):
            swap_type = self.swap_type.value
        elif isinstance(self.swap_type, SymbolSwapTypeType2Type1):
            swap_type = self.swap_type.value
        elif isinstance(self.swap_type, SymbolSwapTypeType3Type1):
            swap_type = self.swap_type.value
        else:
            swap_type = self.swap_type

        margin_initial: Union[None, Unset, str]
        if isinstance(self.margin_initial, Unset):
            margin_initial = UNSET
        else:
            margin_initial = self.margin_initial

        margin_maintenance: Union[None, Unset, str]
        if isinstance(self.margin_maintenance, Unset):
            margin_maintenance = UNSET
        else:
            margin_maintenance = self.margin_maintenance

        margin_per_lot: Union[None, Unset, str]
        if isinstance(self.margin_per_lot, Unset):
            margin_per_lot = UNSET
        else:
            margin_per_lot = self.margin_per_lot

        filling_modes: Union[None, Unset, list[str]]
        if isinstance(self.filling_modes, Unset):
            filling_modes = UNSET
        elif isinstance(self.filling_modes, list):
            filling_modes = []
            for filling_modes_type_0_item_data in self.filling_modes:
                filling_modes_type_0_item = filling_modes_type_0_item_data.value
                filling_modes.append(filling_modes_type_0_item)

        else:
            filling_modes = self.filling_modes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "description": description,
                "server_id": server_id,
                "account_type": account_type,
                "digits": digits,
                "contract_size": contract_size,
                "volume_min": volume_min,
                "volume_max": volume_max,
                "volume_step": volume_step,
                "trade_mode": trade_mode,
                "margin_currency": margin_currency,
                "pip_value_per_lot": pip_value_per_lot,
                "spec_hash": spec_hash,
                "trade_sessions": trade_sessions,
                "refreshed_at": refreshed_at,
                "status": status,
            }
        )
        if profit_currency is not UNSET:
            field_dict["profit_currency"] = profit_currency
        if point is not UNSET:
            field_dict["point"] = point
        if tick_size is not UNSET:
            field_dict["tick_size"] = tick_size
        if tick_value is not UNSET:
            field_dict["tick_value"] = tick_value
        if stops_level is not UNSET:
            field_dict["stops_level"] = stops_level
        if freeze_level is not UNSET:
            field_dict["freeze_level"] = freeze_level
        if swap_long is not UNSET:
            field_dict["swap_long"] = swap_long
        if swap_short is not UNSET:
            field_dict["swap_short"] = swap_short
        if swap_type is not UNSET:
            field_dict["swap_type"] = swap_type
        if margin_initial is not UNSET:
            field_dict["margin_initial"] = margin_initial
        if margin_maintenance is not UNSET:
            field_dict["margin_maintenance"] = margin_maintenance
        if margin_per_lot is not UNSET:
            field_dict["margin_per_lot"] = margin_per_lot
        if filling_modes is not UNSET:
            field_dict["filling_modes"] = filling_modes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.symbol_status import SymbolStatus
        from ..models.trade_session import TradeSession

        d = dict(src_dict)
        symbol = d.pop("symbol")

        description = d.pop("description")

        server_id = UUID(d.pop("server_id"))

        account_type = d.pop("account_type")

        digits = d.pop("digits")

        contract_size = d.pop("contract_size")

        volume_min = d.pop("volume_min")

        volume_max = d.pop("volume_max")

        volume_step = d.pop("volume_step")

        trade_mode = SymbolTradeMode(d.pop("trade_mode"))

        margin_currency = d.pop("margin_currency")

        def _parse_pip_value_per_lot(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pip_value_per_lot = _parse_pip_value_per_lot(d.pop("pip_value_per_lot"))

        spec_hash = d.pop("spec_hash")

        def _parse_trade_sessions(data: object) -> Union[None, list["TradeSession"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trade_sessions_type_0 = []
                _trade_sessions_type_0 = data
                for trade_sessions_type_0_item_data in _trade_sessions_type_0:
                    trade_sessions_type_0_item = TradeSession.from_dict(
                        trade_sessions_type_0_item_data
                    )

                    trade_sessions_type_0.append(trade_sessions_type_0_item)

                return trade_sessions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["TradeSession"]], data)

        trade_sessions = _parse_trade_sessions(d.pop("trade_sessions"))

        refreshed_at = isoparse(d.pop("refreshed_at"))

        status = SymbolStatus.from_dict(d.pop("status"))

        def _parse_profit_currency(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profit_currency = _parse_profit_currency(d.pop("profit_currency", UNSET))

        def _parse_point(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        point = _parse_point(d.pop("point", UNSET))

        def _parse_tick_size(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tick_size = _parse_tick_size(d.pop("tick_size", UNSET))

        def _parse_tick_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tick_value = _parse_tick_value(d.pop("tick_value", UNSET))

        def _parse_stops_level(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stops_level = _parse_stops_level(d.pop("stops_level", UNSET))

        def _parse_freeze_level(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        freeze_level = _parse_freeze_level(d.pop("freeze_level", UNSET))

        def _parse_swap_long(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        swap_long = _parse_swap_long(d.pop("swap_long", UNSET))

        def _parse_swap_short(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        swap_short = _parse_swap_short(d.pop("swap_short", UNSET))

        def _parse_swap_type(
            data: object,
        ) -> Union[
            None, SymbolSwapTypeType1, SymbolSwapTypeType2Type1, SymbolSwapTypeType3Type1, Unset
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                swap_type_type_1 = SymbolSwapTypeType1(data)

                return swap_type_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                swap_type_type_2_type_1 = SymbolSwapTypeType2Type1(data)

                return swap_type_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                swap_type_type_3_type_1 = SymbolSwapTypeType3Type1(data)

                return swap_type_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    SymbolSwapTypeType1,
                    SymbolSwapTypeType2Type1,
                    SymbolSwapTypeType3Type1,
                    Unset,
                ],
                data,
            )

        swap_type = _parse_swap_type(d.pop("swap_type", UNSET))

        def _parse_margin_initial(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        margin_initial = _parse_margin_initial(d.pop("margin_initial", UNSET))

        def _parse_margin_maintenance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        margin_maintenance = _parse_margin_maintenance(d.pop("margin_maintenance", UNSET))

        def _parse_margin_per_lot(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        margin_per_lot = _parse_margin_per_lot(d.pop("margin_per_lot", UNSET))

        def _parse_filling_modes(
            data: object,
        ) -> Union[None, Unset, list[SymbolFillingModesType0Item]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filling_modes_type_0 = []
                _filling_modes_type_0 = data
                for filling_modes_type_0_item_data in _filling_modes_type_0:
                    filling_modes_type_0_item = SymbolFillingModesType0Item(
                        filling_modes_type_0_item_data
                    )

                    filling_modes_type_0.append(filling_modes_type_0_item)

                return filling_modes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[SymbolFillingModesType0Item]], data)

        filling_modes = _parse_filling_modes(d.pop("filling_modes", UNSET))

        symbol = cls(
            symbol=symbol,
            description=description,
            server_id=server_id,
            account_type=account_type,
            digits=digits,
            contract_size=contract_size,
            volume_min=volume_min,
            volume_max=volume_max,
            volume_step=volume_step,
            trade_mode=trade_mode,
            margin_currency=margin_currency,
            pip_value_per_lot=pip_value_per_lot,
            spec_hash=spec_hash,
            trade_sessions=trade_sessions,
            refreshed_at=refreshed_at,
            status=status,
            profit_currency=profit_currency,
            point=point,
            tick_size=tick_size,
            tick_value=tick_value,
            stops_level=stops_level,
            freeze_level=freeze_level,
            swap_long=swap_long,
            swap_short=swap_short,
            swap_type=swap_type,
            margin_initial=margin_initial,
            margin_maintenance=margin_maintenance,
            margin_per_lot=margin_per_lot,
            filling_modes=filling_modes,
        )

        symbol.additional_properties = d
        return symbol

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
