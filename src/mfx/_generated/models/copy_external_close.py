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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyExternalClose")


@_attrs_define
class CopyExternalClose:
    """An external leader closes the position an earlier open made; every follower closes what it copied from it

    Attributes:
        id (str): Your id for this signal
        close (str): The id of the open this closes
        time (Union[None, Unset, datetime.datetime]):
    """

    id: str
    close: str
    time: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        close = self.close

        time: Union[None, Unset, str]
        if isinstance(self.time, Unset):
            time = UNSET
        elif isinstance(self.time, datetime.datetime):
            time = self.time.isoformat()
        else:
            time = self.time

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "close": close,
            }
        )
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        close = d.pop("close")

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

        copy_external_close = cls(
            id=id,
            close=close,
            time=time,
        )

        return copy_external_close
