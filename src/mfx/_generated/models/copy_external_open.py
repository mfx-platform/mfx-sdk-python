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

from ..models.copy_external_open_side import CopyExternalOpenSide
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_external_open_account_type_0 import CopyExternalOpenAccountType0


T = TypeVar("T", bound="CopyExternalOpen")


@_attrs_define
class CopyExternalOpen:
    """An external leader opens a position: a market entry. Exactly one of volume or units; both or neither is refused 422
    unprocessable, details.reason volume_or_units

        Attributes:
            id (str): Your id for this signal, unique for the leader; a close names it
            symbol (str): Your name for the instrument
            side (CopyExternalOpenSide):
            instrument_key (Union[None, Unset, str]): The instrument key in MFX Hub's catalogue, for example fx:EURUSD or
                index:US30; followers' symbols are found by it
            volume (Union[Unset, str]): A decimal as a string, never a JSON number
            units (Union[Unset, str]): A decimal as a string, never a JSON number
            sl (Union[None, Unset, str]):
            tp (Union[None, Unset, str]):
            time (Union[None, Unset, datetime.datetime]): The source's own time for the signal, kept beside MFX Hub's and
                never used for its lifetime
            account (Union['CopyExternalOpenAccountType0', None, Unset]): The source's own account figures where it has
                them; kept with the signal, read by no follower
    """

    id: str
    symbol: str
    side: CopyExternalOpenSide
    instrument_key: Union[None, Unset, str] = UNSET
    volume: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    sl: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    time: Union[None, Unset, datetime.datetime] = UNSET
    account: Union["CopyExternalOpenAccountType0", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_external_open_account_type_0 import (
            CopyExternalOpenAccountType0,
        )

        id = self.id

        symbol = self.symbol

        side = self.side.value

        instrument_key: Union[None, Unset, str]
        if isinstance(self.instrument_key, Unset):
            instrument_key = UNSET
        else:
            instrument_key = self.instrument_key

        volume = self.volume

        units = self.units

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

        time: Union[None, Unset, str]
        if isinstance(self.time, Unset):
            time = UNSET
        elif isinstance(self.time, datetime.datetime):
            time = self.time.isoformat()
        else:
            time = self.time

        account: Union[None, Unset, dict[str, Any]]
        if isinstance(self.account, Unset):
            account = UNSET
        elif isinstance(self.account, CopyExternalOpenAccountType0):
            account = self.account.to_dict()
        else:
            account = self.account

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "symbol": symbol,
                "side": side,
            }
        )
        if instrument_key is not UNSET:
            field_dict["instrument_key"] = instrument_key
        if volume is not UNSET:
            field_dict["volume"] = volume
        if units is not UNSET:
            field_dict["units"] = units
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if time is not UNSET:
            field_dict["time"] = time
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_external_open_account_type_0 import (
            CopyExternalOpenAccountType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        symbol = d.pop("symbol")

        side = CopyExternalOpenSide(d.pop("side"))

        def _parse_instrument_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instrument_key = _parse_instrument_key(d.pop("instrument_key", UNSET))

        volume = d.pop("volume", UNSET)

        units = d.pop("units", UNSET)

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

        def _parse_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_type_0 = isoparse(data)

                return time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        time = _parse_time(d.pop("time", UNSET))

        def _parse_account(data: object) -> Union["CopyExternalOpenAccountType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                account_type_0 = CopyExternalOpenAccountType0.from_dict(data)

                return account_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyExternalOpenAccountType0", None, Unset], data)

        account = _parse_account(d.pop("account", UNSET))

        copy_external_open = cls(
            id=id,
            symbol=symbol,
            side=side,
            instrument_key=instrument_key,
            volume=volume,
            units=units,
            sl=sl,
            tp=tp,
            time=time,
            account=account,
        )

        return copy_external_open
