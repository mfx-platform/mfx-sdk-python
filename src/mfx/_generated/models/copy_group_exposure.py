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

if TYPE_CHECKING:
    from ..models.copy_group_exposure_leavers import CopyGroupExposureLeavers


T = TypeVar("T", bound="CopyGroupExposure")


@_attrs_define
class CopyGroupExposure:
    """A group's gross exposure against its cap, every figure in US dollars to the cent. Recorded from the copy hosts'
    answers behind the send, so a few seconds behind them. Each exposure is fixed at its copy's open (its price and rate
    then); a close lowers it by the fraction closed.

        Attributes:
            cap (Union[None, str]): gross_exposure_cap; null is no cap
            used (str): The exposure of the live members' open copied positions
            share (Union[None, str]): Each live member's signed share: the cap over members, rounded down to the cent; null
                with no cap or no live member
            members (int): The live members the cap is shared by (followers_live)
            unpriced (int): Open copied positions not in used: opened before exposure was recorded, or priced in another
                currency
            leavers (CopyGroupExposureLeavers): The open copied positions of followers that left the group (unfollowed
                without close_copied, or removed): copied under it, no longer counted in used or against the cap
            unenforced (int): Live members whose account runs on a host that cannot enforce its share yet (a copy host older
                than the release that enforces it, or one that does not report its version): their copies are not held to the
                share, so used can pass the cap
            as_of (datetime.datetime): When it was read
    """

    cap: Union[None, str]
    used: str
    share: Union[None, str]
    members: int
    unpriced: int
    leavers: "CopyGroupExposureLeavers"
    unenforced: int
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_exposure_leavers import CopyGroupExposureLeavers

        cap: Union[None, str]
        cap = self.cap

        used = self.used

        share: Union[None, str]
        share = self.share

        members = self.members

        unpriced = self.unpriced

        leavers = self.leavers.to_dict()

        unenforced = self.unenforced

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cap": cap,
                "used": used,
                "share": share,
                "members": members,
                "unpriced": unpriced,
                "leavers": leavers,
                "unenforced": unenforced,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_exposure_leavers import CopyGroupExposureLeavers

        d = dict(src_dict)

        def _parse_cap(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        cap = _parse_cap(d.pop("cap"))

        used = d.pop("used")

        def _parse_share(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        share = _parse_share(d.pop("share"))

        members = d.pop("members")

        unpriced = d.pop("unpriced")

        leavers = CopyGroupExposureLeavers.from_dict(d.pop("leavers"))

        unenforced = d.pop("unenforced")

        as_of = isoparse(d.pop("as_of"))

        copy_group_exposure = cls(
            cap=cap,
            used=used,
            share=share,
            members=members,
            unpriced=unpriced,
            leavers=leavers,
            unenforced=unenforced,
            as_of=as_of,
        )

        copy_group_exposure.additional_properties = d
        return copy_group_exposure

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
